#include<bits/stdc++.h>
using namespace std;

int v[123][123];
int n,m;
int _,__,___;
signed main(){
    ios::sync_with_stdio(0);
    memset(v,0x3f,sizeof(v));
    cin >> n >> m;
    for(int i=1; i<=m; i++){
        cin >> _ >> __ >> ___;
        v[_][__]=min(v[_][__],___);
        v[__][_]=min(v[__][_],___);
    }
    for(int i=1; i<=n; i++) v[i][i]=0;
    for(int k=1; k<=n; k++){
        for(int i=1; i<=n; i++){
            for(int j=1; j<=n; j++){
                if(v[i][k]+v[k][j]<v[i][j]){
                    v[i][j]=v[i][k]+v[k][j];
                }
            }
        }
    }
    for(int i=1; i<=n; i++){
        for(int j=1; j<=n; j++){
            cout << v[i][j] << " ";
        }
        cout << "\n";
    }
    return 0;
}