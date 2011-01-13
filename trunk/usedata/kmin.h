#ifndef KMIN_H_
#define KMIN_H_

/************************************************************************/
/*   min k values problem with maxheap data structure                   */
/*            the computation cost is nlog(k)                           */
/*----------------------------------------------------------------------*/
/*   void kmin_maxheap(Tnum * a,long int n,Tnum*b,int k)                */
/*   void kmin_idx_maxheap(Tnum * a,long int n,Tnum*b,int k,Tint *idx)  */
/*----------------------------------------------------------------------*/
/*   a is the input array of length n                                   */
/*   b stores the k maximum values                                      */
/*   idx stores the indice of entries of b corresponding to a           */
/*----------------------------------------------------------------------*/
/*   written by Zhao Keke.                                              */
/*            Aug 20, 2010. modified at December 15, 2010.              */
/************************************************************************/

//----min k values problem by maxheap---//
template<typename Tnum>
void make_maxheap(Tnum*b,int k)
{
	/*
	Tnum tmp;register int i,j,n;

	for (n=1;n<k;n++){// insert_maxheap: MoveUp			
		j=n;i=(j-1)>>1;
		while(i>=0){
			if(b[i]<b[j]){
				tmp=b[i];b[i]=b[j];b[j]=tmp;
				j=i;i=(j-1)>>1; // parent
			}else break;
		}
	}
	*/
	for (register int i=((k-1)-1)>>1;i>=0;i--){
		down_maxheap(b,k,i);
	}
	
}

template<typename Tnum>
void down_maxheap(Tnum*b,int k,int parent=0)
{ 
	Tnum tmp;register int i,j;

	i=parent;j=(i<<1)+1;
	while(j+1<k){
		if(b[j]<b[j+1])j++;
		if(b[i]>=b[j])break;
		tmp=b[i];b[i]=b[j];b[j]=tmp;
		i=j;j=(j<<1)+1; // j=j*2+1;
	}
	if(j<k&&b[i]<b[j]){
		tmp=b[i];b[i]=b[j];b[j]=tmp;
	}
}
template<typename Tnum>
void sort_maxheap(Tnum*b,int k)
{  
	register int i;Tnum tmp;
	while(k-->0){
		tmp=b[0];b[0]=b[k];b[k]=tmp;
		down_maxheap(b,k);
	}
}
template<typename Tnum>
void kmax_maxheap(Tnum * a,long int n,Tnum*b,int k)
{
	if (!(k<=n&&k>0)){return;}

	for (int j=0;j<k;j++){b[j]=a[j];}
	make_maxheap(b,k);
	for (register long int i=k;i<n;i++)
		if(a[i]<b[0]){
			b[0]=a[i];
			down_maxheap(b,k);
		}
	//we may sort the resulting array
	sort_maxheap(b,k);
}


//----min k values problem with index----//
template<typename Tnum,typename Tint>
void make_maxheap_idx(Tnum*b,int k,Tint*idx){
	/*
	Tnum tmp;Tint tmp_idx;register int i,j,n;

	for (n=1;n<k;n++){// insert_maxheap_idx: MoveUp	
		j=n;i=(j-1)>>1;
		while(i>=0){
			if(b[i]<b[j]){
				tmp=b[i];b[i]=b[j];b[j]=tmp;
				tmp_idx=idx[i];idx[i]=idx[j];idx[j]=tmp_idx;
				j=i;i=(j-1)>>1; // parent
			}else break;
		}
	}*/
	for (register int i=((k-1)-1)>>1;i>=0;i--){
		down_maxheap_idx(b,k,idx,i);
	}
}

template<typename Tnum,typename Tint>
void down_maxheap_idx(Tnum*b,int k,Tint*idx,int parent=0)
{ 
	Tnum tmp;Tint tmp_idx;register int i,j;

	i=parent;j=(i<<1)+1;
	while(j+1<k){
		if(b[j]<b[j+1])j++;
		if(b[i]>=b[j])break;
		tmp=b[i];b[i]=b[j];b[j]=tmp;
		tmp_idx=idx[i];idx[i]=idx[j];idx[j]=tmp_idx;
		i=j;j=(j<<1)+1; // j=j*2+1;
	}
	if(j<k&&b[i]<b[j]){
		tmp=b[i];b[i]=b[j];b[j]=tmp;
		tmp_idx=idx[i];idx[i]=idx[j];idx[j]=tmp_idx;
	}
}
template<typename Tnum,typename Tint>
void sort_maxheap_idx(Tnum*b,int k,Tint *idx)
{  
	register int i;Tnum tmp;Tint tmp_idx;
	while(k-->0){
		tmp=b[0];b[0]=b[k];b[k]=tmp;
		tmp_idx=idx[0];idx[0]=idx[k];idx[k]=tmp_idx;
		down_maxheap_idx(b,k,idx);
	}
}
template<typename Tnum,typename Tint>
void kmax_idx_maxheap(Tnum * a,long int n,Tnum*b,int k,Tint *idx)
{
	if (!(k<=n&&k>0)){return;}

	for (int j=0;j<k;j++){b[j]=a[j];idx[j]=j;}
	make_maxheap_idx(b,k,idx);
	for (register Tint i=k;i<n;i++)
		if(a[i]<b[0]){
			b[0]=a[i];idx[0]=i;
			down_maxheap_idx(b,k,idx);
		}
	//we may sort the resulting array
	sort_maxheap_idx(b,k,idx);
}

#endif
