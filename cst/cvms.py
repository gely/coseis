"""
SCEC Community Velocity Model - Magistrale version
"""
import os
import json
import copy
import shutil
import subprocess
import numpy
from . import home
from . import job

repository = home + 'repo'
versions = ['2.2', '3.0', '4.0']

input_template = """\
{nsample}
{file_lon}
{file_lat}
{file_dep}
{file_rho}
{file_vp}
{file_vs}
"""

defaults = {
    'version': '4.0',
    'file_dep': 'mesh-dep.bin',
    'file_lat': 'mesh-lat.bin',
    'file_lon': 'mesh-lon.bin',
    'file_rho': 'mesh-rho.bin',
    'file_vp': 'mesh-vp.bin',
    'file_vs': 'mesh-vs.bin',
    'max_samples': 4800000,
    'minutes': 60,
    'nsample': 0,
    'nthread': 1,
    'machine_opts': {
        'alcf_bgq_dev': {'mode': 'vn'},
        'alcf_bgq_mira': {'mode': 'vn'},
    },
}


def configure(force=False, **kw):

    cwd = os.getcwd()
    os.chdir(repository)

    cfg = copy.deepcopy(defaults)
    cfg = job.prepare(
        defaults=cfg,
        name='cvms',
        executable=os.path.join('.', 'cvms.x'),
        **kw
    )

    for k, d in cfg['machine_opts'].items():
        if k in cfg['machine']:
            for k, v in d.items():
                cfg[k] = v

    ver = cfg['version']
    if ver is None:
        cfg['version'] = ver = versions[-1]
    else:
        assert ver in versions

    bld = 'build-%s' % ver + os.sep
    if not os.path.exists(bld):
        os.mkdir(bld)
        p = os.path.join(repository, 'CVMS-%s' % ver, 'src') + os.sep
        for f in os.listdir(p):
            shutil.copy2(p + f, bld + f)

    f = open('in.h.in').read()
    f = f.format(max_samples=cfg['max_samples'])
    open(bld + 'in.h', 'w').write(f)

    m = open('Makefile.in').read()
    m = m.format(machine=cfg['machine'])
    open(bld + 'Makefile', 'w').write(m)

    os.chdir(cwd)

    return cfg


def make(force=False, **kwargs):
    cfg = configure(force, **kwargs)
    p = os.path.join(__file__[:-3], 'build-%s' % cfg['version']) + os.sep
    if force:
        subprocess.check_call(['make', '-C', p, 'clean'])
    subprocess.check_call(['make', '-C', p, '-j', '2'])
    c = json.load(open(p + 'config.json'))
    cfg.update(c)
    return cfg


def run(**kwargs):
    cfg = make(**kwargs)

    p = (cfg['nsample'] - 1) // cfg['max_samples'] + 1
    n = (cfg['nsample'] - 1) // cfg['nproc'] + 1
    if p > cfg['nproc']:
        raise Exception(
            'nsample = %s requires nproc >= %s or max_samples >= %s' %
            (cfg['nsample'], p, n)
        )

    if cfg['process'] == 'serial':
        cfg['execute'] = cfg['executable']

    p = os.path.join(repository, 'CVMS-%s' % cfg['version'], 'data')
    for f in os.listdir(p):
        g = os.path.join(p, f)
        os.link(g, f)

    f = os.path.join(__file__[:-3], 'build-%s' % cfg['version'], 'cvms.x')
    os.link(f, 'cvms.x')

    open('cvms.in', 'w').write(input_template.format(**cfg))
    job.launch(cfg)

    return cfg


def extract(lon, lat, dep, prop=['rho', 'vp', 'vs'], **kwargs):
    """
    Simple CVM-S extraction

    lon, lat, dep: Coordinate arrays
    prop: 'rho', 'vp', or 'vs'
    nproc: Optional, number of processes
    Returns: (rho, vp, vs) material arrays
    """

    lon = numpy.asarray(lon, 'f')
    lat = numpy.asarray(lat, 'f')
    dep = numpy.asarray(dep, 'f')
    shape = dep.shape
    nsample = dep.size

    cwd = os.getcwd()
    if os.path.exists('cvms-tmp'):
        shutil.rmtree('cvms-tmp')
    os.mkdir('cvms-tmp')
    os.chdir('cvms-tmp')

    cfg = configure(**kwargs)

    lon.tofile(cfg['file_lon'])
    lat.tofile(cfg['file_lat'])
    dep.tofile(cfg['file_dep'])
    del(lon, lat, dep)

    run(nsample=nsample, **kwargs)

    out = []
    if type(prop) not in [list, tuple]:
        prop = [prop]
    for v in prop:
        f = cfg['file_' + v.lower()]
        out += [numpy.fromfile(f, 'f').reshape(shape)]

    os.chdir(cwd)
    shutil.rmtree('cvms-tmp')

    return out
