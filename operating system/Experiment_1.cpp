#include<bits/stdc++.h>
using namespace std;
const int MaxNum=100;
int  ArrivalTime[MaxNum];
int  ServiceTime[MaxNum];
int  FinishTime[MaxNum];
int  WholeTime[MaxNum];
double  WeightWholeTime[MaxNum];
double AverageWT_FCFS,AverageWT_SJF,SumWT_FCFS,SumWT_SJF; 
double AverageWWT_FCFS,AverageWWT_SJF,SumWWT_FCFS,SumWWT_SJF;

void init(){
    memset(ArrivalTime,0,sizeof(ArrivalTime));
    memset(ServiceTime,0,sizeof(ServiceTime));
}
int n,op;
struct node{
    int arr,ser,num;
}tlist[MaxNum];

struct cmp{
    bool operator()(const node &a,const node &b)const{
        if(a.ser!=b.ser) return a.ser>b.ser;
        return a.arr>b.arr;
    }
};
void fcfs(){
    queue<node> q;
    for(int i=1; i<=n; i++){
        tlist[i].arr=ArrivalTime[i];
        tlist[i].ser=ServiceTime[i];
        tlist[i].num=i;
    }
    sort(tlist+1,tlist+1+n,[](const node &a,const node &b)-> bool {
        return a.arr<b.arr;
    });
    int t=0;
    for(int i=1; i<=n; i++){
        if(!q.empty()){
            node k=q.front();
            while(tlist[i].arr>t+k.ser){
                t+=k.ser;
                q.pop();
                FinishTime[k.num]=t;
                if(!q.empty()){
                    k=q.front();
                }else{
                    t=tlist[i].arr;
                    break;
                }
            }
        }else t=tlist[i].arr;
        q.push(tlist[i]);
    }
    while(!q.empty()){
        node k=q.front();
        t+=k.ser;
        FinishTime[k.num]=t;
        q.pop();
    }
    SumWT_FCFS=0;
    SumWWT_FCFS=0;
    for(int i=1; i<=n; i++){
        WholeTime[i]=FinishTime[i]-ArrivalTime[i];
        SumWT_FCFS+=WholeTime[i];
        WeightWholeTime[i]=(double)WholeTime[i]/ServiceTime[i];
        SumWWT_FCFS+=WeightWholeTime[i];
    }
    AverageWT_FCFS=SumWT_FCFS/n;
    AverageWWT_FCFS=SumWWT_FCFS/n;
}
void sjf(){
    for(int i=1; i<=n; i++){
        tlist[i].arr=ArrivalTime[i];
        tlist[i].ser=ServiceTime[i];
        tlist[i].num=i;
    }
    sort(tlist+1,tlist+1+n,[](const node &a,const node &b)-> bool {
        return a.arr<b.arr;
    });
    priority_queue<node,vector<node>,cmp> q;
    int t=0,i=1;
    while(i<=n||!q.empty()){
        if(q.empty()&&i<=n&&t<tlist[i].arr) t=tlist[i].arr;
        while(i<=n&&tlist[i].arr<=t) q.push(tlist[i++]);
        node k=q.top();
        q.pop();
        t+=k.ser;
        FinishTime[k.num]=t;
    }
    SumWT_SJF=0;
    SumWWT_SJF=0;
    for(int i=1; i<=n; i++){
        WholeTime[i]=FinishTime[i]-ArrivalTime[i];
        SumWT_SJF+=WholeTime[i];
        WeightWholeTime[i]=(double)WholeTime[i]/ServiceTime[i];
        SumWWT_SJF+=WeightWholeTime[i];
    }
    AverageWT_SJF=SumWT_SJF/n;
    AverageWWT_SJF=SumWWT_SJF/n;
}

//打印表让deepseek写的
void printResult(const string &name,double avgWT,double avgWWT){
    cout<<fixed<<setprecision(2);
    cout<<"\n===== "<<name<<" =====\n";
    cout<<"Process\tArrival\tService\tFinish\tTurnaround\tWeighted\n";
    for(int i=1; i<=n; i++){
        cout<<i<<"\t"<<ArrivalTime[i]<<"\t"<<ServiceTime[i]<<"\t"
            <<FinishTime[i]<<"\t"<<WholeTime[i]<<"\t\t"<<WeightWholeTime[i]<<"\n";
    }
    cout<<"Average Turnaround Time          : "<<avgWT<<"\n";
    cout<<"Average Weighted Turnaround Time : "<<avgWWT<<"\n";
}
signed main(){
    init();
    cin >> n;
    for(int i=1; i<=n; ++i){
        cin >> ArrivalTime[i];
    }
    for(int i=1; i<=n; ++i){
        cin >> ServiceTime[i];
    }
    while(1){
        cin >> op;
        if(op==1){
            fcfs();
            printResult("FCFS",AverageWT_FCFS,AverageWWT_FCFS);
        }else{
            sjf();
            printResult("SJF",AverageWT_SJF,AverageWWT_SJF);
        }
    }
    return 0;
}