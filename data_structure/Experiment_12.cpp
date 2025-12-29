#include<bits/stdc++.h>
using namespace std;
const int M=2e5+500;
int n,m,ans;
bool op;
struct node{
	int a,b,v;
	bool operator <(const node &p)const{
		return p.v>v;
	}
}edge[M];
int pre[5500];
int fa(int x){
	if(pre[x]==x) return x;
	pre[x]=fa(pre[x]);
	return pre[x];
}
void kruskal(){
	int f1,f2,k=0;
	for(int i=1; i<=m; i++){
		f1=fa(edge[i].a);
		f2=fa(edge[i].b);
		if(f1!=f2){
			ans+=edge[i].v;
			pre[f1]=f2;
			k++;
			if(k==n-1){
				break;
			} 
		}
	}
	if(k<n-1) {
		printf("orz");
		op=1;
		return;
	}
}
int main(){
	scanf("%d%d",&n,&m);
	for(int i=1; i<=m; i++){
		scanf("%d%d%d",&edge[i].a,&edge[i].b,&edge[i].v);
	}
	sort(edge+1,edge+1+m);
	for(int i=1; i<=n; i++){
		pre[i]=i;
	}
	kruskal();
	if(!op) printf("%d",ans);
	return 0; 
}