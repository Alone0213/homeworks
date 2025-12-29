#include<bits/stdc++.h>
using namespace std;

int n;
int v[123][123];
int a[123][123];
bool vis[123];
int p,cnt;
int ans[123];
int check(){
    for(int i=1; i<=n; i++){
        if(!vis[i]&&v[i][0]==0){
            vis[i]=1;
            p=i;
            return p;
        }
    }
    p=0;
    return p;
}
signed main(){
    cin >> n;
    for(int i=1; i<=n; i++){
        int _=1;
        while(_!=0){
            cin >> _;
            if(!_) break;
            v[i][_]=1;
            a[_][i]=1;
            v[i][0]++;
        }
    }
    while(check()!=0){
        for(int i=1; i<=n; i++){
            if(a[p][i]){
                v[i][0]--;
            }
        }
        ans[++cnt]=p;
    }
    for(int i=n; i; i--){
        cout << ans[i] << " ";
    }
    return 0;
}