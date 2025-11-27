#include<bits/stdc++.h>
using namespace std;
typedef struct triple{
    int r,c,val;
}tri;
struct rdexlist{
    tri ele[2500];
    int rnum,cnum,trnum;
    int rpos[50];
};

rdexlist t1,t2,m;
signed main(){
    int in;
    printf("请输入A的行数和列数，两者中间空一格：\n");
    cin >> t1.rnum >> t1.cnum;
    printf("请输入矩阵：\n");
    for(int i=1; i<=t1.rnum; i++){
        t1.rpos[i]=t1.trnum+1;
        for(int j=1; j<=t1.cnum; j++){
            cin >> in;
            if(in){
                t1.trnum++;
                t1.ele[t1.trnum].r=i;
                t1.ele[t1.trnum].c=j;
                t1.ele[t1.trnum].val=in;
            }
        }
    }
    printf("请输入B的行数和列数，两者中间空一格：\n");
    cin >> t2.rnum >> t2.cnum;
    printf("请输入矩阵：\n");
    for(int i=1; i<=t2.rnum; i++){
        t2.rpos[i]=t2.trnum+1;
        for(int j=1; j<=t2.cnum; j++){
            cin >> in;
            if(in){
                t2.trnum++;
                t2.ele[t2.trnum].r=i;
                t2.ele[t2.trnum].c=j;
                t2.ele[t2.trnum].val=in;
            }
        }
    }
    int csum_perrow[50];
    if(t1.trnum*t2.trnum)
    for(int i=1; i<=t1.rnum; i++){
        memset(csum_perrow,0,sizeof(csum_perrow));
        if(t1.cnum!=t2.rnum){
            printf("Error,行数列数不匹配\n");
            exit(0);
        }
        m.rpos[i]=m.trnum+1;
        for(int j=t1.rpos[i]; j<(i==t1.rnum?t1.trnum+1:t1.rpos[i+1]); j++){
            int crt_col=t1.ele[j].c;
            for(int k=t2.rpos[crt_col]; k<(crt_col==t2.rnum?t2.trnum+1:t2.rpos[crt_col+1]); k++){
                int t2col=t2.ele[k].c;
                csum_perrow[t2col]+=t1.ele[j].val*t2.ele[k].val;
            }
        }
        for(int mcol=1; mcol<=t2.cnum; mcol++){
            if(csum_perrow[mcol]){
                m.ele[++m.trnum]={i,mcol,csum_perrow[mcol]};
            }
        }
    }
    printf("乘积矩阵非零元为：\n");
    for(int i=1; i<=m.trnum; i++){
        printf("%d %d %d\n",m.ele[i].r,m.ele[i].c,m.ele[i].val);
    }
    return 0;
}