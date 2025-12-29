#include<bits/stdc++.h>
#define int long long
using namespace std;
const int M=2e5+972;
const int N=1e5+853;
int n,m,s;
int _,__,___;

struct node{
	int ne,to,w;
}g[M];int h[N];int cnt;

void add(int a,int b,int c){
	g[++cnt].ne=h[a];
	g[cnt].to=b;
	g[cnt].w=c;
	h[a]=cnt;
}

priority_queue<pair<int,int>,vector<pair<int,int> >,greater<pair<int,int> > > q;
int dis[N];
bool vis[N];
void dijkstra(){
	for(int i=1; i<=n; i++) dis[i]=0x7fffffff,vis[i]=0;
	q.push(make_pair(0,s));
	dis[s]=0;
	while(!q.empty()){
		int u=q.top().second;
		q.pop();
		if(vis[u]) continue;
		vis[u]=1;
		for(int i=h[u]; i; i=g[i].ne){
			int v=g[i].to;
			if(dis[v]>dis[u]+g[i].w){
				dis[v]=dis[u]+g[i].w;
				q.push(make_pair(dis[v],v));
			}
		}
	}
	for(int i=1; i<=n; i++){
		printf("%lld ",dis[i]);
	}
}

signed main(){
	scanf("%lld%lld%lld",&n,&m,&s);
	for(int i=1; i<=m; i++){
		scanf("%lld%lld%lld",&_,&__,&___);
		add(_,__,___);
	}
	dijkstra();
	return 0;
}