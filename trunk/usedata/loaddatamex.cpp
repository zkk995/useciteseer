#include <stdio.h>
#include <stdlib.h>
#include "mex.h"
#include <string>

#include"kmin.h"

int load_bin(char *path, void *data, int len)/*load bin file*/ {
    FILE *fp;
    printf("Loading %s\n", path);
    fp=fopen(path, "rb");
    if(!fp) {
        printf("Cant open file\n");
        return 0;
    }
    if(len!=fread(data, 1, len, fp)) {
        printf("Failed to read all data\n");
        return 0;
    }
    fclose(fp);
    return 1;
}

void dump_bin(char *path, void *data, int len)/* write data into bin file */ {
    FILE *fp;
    printf("Writing %s\n", path);
    fp=fopen(path, "wb");
    if(len!=fwrite(data, 1, len, fp)) {
        printf("Failed to write all data\n");
        exit(1);
    }
    fclose(fp);
}

int load_text(char*path, int*x, int len) {
    FILE *fp;int i;
    printf("Loading %s\n", path);
    fp=fopen(path, "r");
    if(!fp){
        printf("Can't open file \n");
        return 0;
    }
    for(i=0;i<len;i++){
        fscanf(fp, "%d", x+i);
    }
    fclose(fp);
    return 1;
}

/* A =itemsparse(); */

void mexFunction(int nlhs, mxArray *plhs[],
        int nrhs, const mxArray *prhs[]) {
    if(nlhs!=1||nrhs!=1){
        mexErrMsgTxt("usage: A =loaddatamex(path) ");
    }
    std::string path((char *)mxArrayToString(prhs[0]));
    if( !path.empty()){path+="/";}
    std::string txtfile=path+"word_doc_entry.txt",
            jcfile=path+"Jc.bin",
            irfile=path+"Ir.bin";
    
    int m, n, nnz;int *m_n_nnz=new int [3];
    if(!load_text((char *)txtfile.c_str(), m_n_nnz, 3)){
        mexErrMsgTxt("error in loading m,n,nnz ");
    }
    m=m_n_nnz[0];n=m_n_nnz[1];nnz=m_n_nnz[2];delete [] m_n_nnz;
    
    int *Ir_ = new int[nnz];
    int *Jc_ = new int[n+1]; {
        if(!load_bin((char *)jcfile.c_str(), Jc_, (n+1)*sizeof(int))||
                !load_bin((char *)irfile.c_str(), Ir_, nnz*sizeof(int))){
            mexErrMsgTxt("error in loading Jc,Ir");
        }
    }
    plhs[0] = mxCreateSparse(m, n, nnz, mxREAL);
    double  *sr = mxGetPr(plhs[0]);
    mwIndex *Ir = mxGetIr(plhs[0]);
    mwIndex *Jc = mxGetJc(plhs[0]);
    for(int i=0;i<n+1;i++)Jc[i] =Jc_[i];
    for(int i=0;i<nnz;i++){Ir[i] =Ir_[i];sr[i]=1;}
	for(int j=0;j<n;j++){
	
	// sort by index
	make_maxheap_idx(Ir+Jc[j],Jc[j+1]-Jc[j],sr+Jc[j]);
	sort_maxheap_idx(Ir+Jc[j],Jc[j+1]-Jc[j],sr+Jc[j]);
	}
	
    delete [] Ir_, Jc_;
    
#ifdef DEBUG
for(int i=0;i<n+1;i++)
    mexPrintf("Jc %d\n", Jc[i]);
#endif
}

/*
 * std::string txtfile(path), jcfile(path), irfile(path);
 * txtfile.append("word_doc_entry.txt");
 * jcfile.append("Jc.bin");
 * irfile.append("Ir.bin");
 */