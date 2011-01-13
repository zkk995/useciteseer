function [R,key] =loadCiteSeer(mpath)
% relation matrix
% v2£¿
if ~isempty(mpath),
    mpath=[mpath,'/'];
end
fp=fopen([mpath,'databin/info.txt']);
F=textscan(fp,'%s');
fclose(fp);

key=F{1};

R = loaddatamex([mpath,'databin/']);
% DD=max(DD,DD');
% 
% R=DD;
% 
% for i=1:3
%     d=sum(R,2);d=full(d);
%     sJ= d>(50-i*5);
%     R=DD(sJ,sJ);
% end


return
%%
% mex loaddatamex.cpp -largeArrayDims

[DD,key,sJ,R]=loadCiteSeer('');


d=sum(R);d=full(d);
plot(sort(d))