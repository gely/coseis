%------------------------------------------------------------------------------%
% DCNR - cell-to-node rectangular grid difference operator

function df = dcnr( f, i, x, a, j, k, l )
switch a
case 1
df = 1 / 4 * ...
((x(j,k,l+1,3)-x(j,k,l,3)).*((x(j,k+1,l,2)-x(j,k,l,2)).*(f(j,k,l,i)-f(j-1,k,l,i))+(x(j,k,l,2)-x(j,k-1,l,2)).*(f(j,k-1,l,i)-f(j-1,k-1,l,i)))...
+(x(j,k,l,3)-x(j,k,l-1,3)).*((x(j,k+1,l,2)-x(j,k,l,2)).*(f(j,k,l-1,i)-f(j-1,k,l-1,i))+(x(j,k,l,2)-x(j,k-1,l,2)).*(f(j,k-1,l-1,i)-f(j-1,k-1,l-1,i))));
case 2
df = 1 / 4 * ...
((x(j+1,k,l,1)-x(j,k,l,1)).*((x(j,k,l+1,3)-x(j,k,l,3)).*(f(j,k,l,i)-f(j,k-1,l,i))+(x(j,k,l,3)-x(j,k,l-1,3)).*(f(j,k,l-1,i)-f(j,k-1,l-1,i)))...
+(x(j,k,l,1)-x(j-1,k,l,1)).*((x(j,k,l+1,3)-x(j,k,l,3)).*(f(j-1,k,l,i)-f(j-1,k-1,l,i))+(x(j,k,l,3)-x(j,k,l-1,3)).*(f(j-1,k,l-1,i)-f(j-1,k-1,l-1,i))));
case 3
df = 1 / 4 * ...
((x(j,k+1,l,2)-x(j,k,l,2)).*((x(j+1,k,l,1)-x(j,k,l,1)).*(f(j,k,l,i)-f(j,k,l-1,i))+(x(j,k,l,1)-x(j-1,k,l,1)).*(f(j-1,k,l,i)-f(j-1,k,l-1,i)))...
+(x(j,k,l,2)-x(j,k-1,l,2)).*((x(j+1,k,l,1)-x(j,k,l,1)).*(f(j,k-1,l,i)-f(j,k-1,l-1,i))+(x(j,k,l,1)-x(j-1,k,l,1)).*(f(j-1,k-1,l,i)-f(j-1,k-1,l-1,i))));
end
%flops: 7* 31+

