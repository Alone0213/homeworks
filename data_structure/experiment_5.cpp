#include<bits/stdc++.h>
using namespace std;
const int N=103;
bool c_isempty=1;
bool n_isempty=1;
int cpt;
int npt;
char opts[N];
int nums[N];
int tmp;

bool t;
bool lastc;

signed main(){
    char c=getchar();
    while(c!='\n'){
        t=0;
        if(c>='0'&&c<='9'){
            tmp=(tmp<<1)+(tmp<<3);
            tmp+=c-'0';
        }else{
            if(c=='(') opts[++cpt]=c;
            if(c=='*'||c=='/'||c=='+'||c=='-'){
                if(!lastc){
                    nums[++npt]=tmp;tmp=0;
                }
                if(opts[cpt]=='*'||opts[cpt]=='/'){
                    char ctop=opts[cpt];cpt--;
                    int a1=nums[npt];npt--;
                    int a2=nums[npt];npt--;
                    if(ctop=='*') nums[++npt]=a1*a2;
                    if(ctop=='/') nums[++npt]=a2/a1;
                }
                opts[++cpt]=c;
                lastc=0;
            }
            if(c==')'){
                lastc=1;
                nums[++npt]=tmp;tmp=0;
                t=1;
                char ctop=opts[cpt];cpt--;
                while(ctop!='('){
                    int a1=nums[npt];npt--;
                    int a2=nums[npt];npt--;
                    if(ctop=='+') nums[++npt]=a1+a2;
                    if(ctop=='-') nums[++npt]=a2-a1;
                    if(ctop=='*') nums[++npt]=a1*a2;
                    if(ctop=='/') nums[++npt]=a2/a1;
                    ctop=opts[cpt];cpt--;
                }
            }
        }
        npt?n_isempty=0:n_isempty=1;
        cpt?c_isempty=0:c_isempty=1;
        c=getchar();
    }
    if(!t)  nums[++npt]=tmp;
    while(!c_isempty){
        char ctop=opts[cpt];cpt--;
        int a1=nums[npt];npt--;
        int a2=nums[npt];npt--;
        if(ctop=='+') nums[++npt]=a1+a2;
        if(ctop=='-') nums[++npt]=a2-a1;
        if(ctop=='*') nums[++npt]=a1*a2;
        if(ctop=='/') nums[++npt]=a2/a1;
        cpt?c_isempty=0:c_isempty=1;
        npt?n_isempty=0:n_isempty=1;
    }
    int ans=nums[npt];npt--;
    printf("%d\n",ans);
    return 0;
}