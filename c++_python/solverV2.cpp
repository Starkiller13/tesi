#include<iostream>
#include<fstream>
#include<strings.h>
#include <ilcplex/cplex.h>
#include <ilcplex/ilocplex.h>
ILOSTLBEGIN

char * f = (char *) malloc(1000);
int i,j,clique_counter;
bool isClique = true;

int main(int argc, char **argv){
   IloEnv env;
   IloModel model(env);
   IloModel modelRelaxed(env);
   IloObjective obj;
   IloNumVar tmp(env);
   IloNumVarArray var(env);
   IloRangeArray rng(env);
   IloCplex cplex(model);
   IloExpr::LinearIterator it;
   IloNum ref = IloNum(0);
   ofstream myfile;
   strcat(f,"data/");
   strcat(f,argv[1]);
   strcat(f,".txt");
   try{
      cplex.importModel(model,argv[1],obj,var,rng);
      myfile.open(f);
   }catch(IloException& e){
      cerr << "Error importing model, aborting..." << endl << e << endl;
      return 1;
   }catch(...){
      cerr << "Generic exception, aborting..." << endl ;
      return 1;
   }
   /*array in cui salvo la posizione dei vincoli di clique
     a modo di bucket*/
   int cliques[rng.getSize()];
   for(i = 0;i < rng.getSize(); i++){
      cliques[i] = 0;
   }
   /*Preprocesso il probelma per trovare vincoli di clique
     se sono presenti*/
   for(i = 0;i < rng.getSize(); i++){
      it = rng[i].getLinearIterator();
      while(it.ok()){
            if(it.getVar().getType()!=IloNumVar::Type::Bool||it.getCoef()!=IloNum(1)){
               isClique = false;
            }
            ++it;
      }
      if(isClique)  
         if(rng[i].getUb()==IloNum(1)){
            //Vincolo <=
            if(rng[i].getLb()==IloNum(0)){
               cliques[i] = 2;
               clique_counter++;
            }
            //Vincolo ==
            else if(rng[i].getLb()==IloNum(1)){
               cliques[i] = 1;
               clique_counter++;
            }
         }
      isClique = true;
   }   
   /*Se il problema non ha vincoli di clique lo scarto*/
   if(clique_counter==0){
      cout << "Problem has no clique constraints, exiting!" << endl;
      myfile << "MIP: " << argv[1] << endl << "-- Not very interesting --"<< endl;
      return 0;
   }
   modelRelaxed.add(rng);
   modelRelaxed.add(obj);
   for(i = 0;i < var.getSize();i++){
      modelRelaxed.add(IloConversion(env,var[i],ILOFLOAT));
   }
   IloCplex cplexR(modelRelaxed);
   cplexR.setParam(IloCplex::PreInd, false);
   /*Risolvo il rilassaento senza modifiche*/
    if(!cplexR.solve()){
        cerr << "Something went wrong" << endl;
        return 1;
    }
    ref = cplexR.getObjValue();
   /*Se il vincolo è di <= risolvo il rilassamento impostand
     tutte le varibili del vincolo a 0*/
    j=0;
    myfile << "MIP: " << argv[1] << endl;
    myfile << "LP relaxation result: " << ref << endl << endl; 
    for(i = 0; i < rng.getSize(); i++){
        if(cliques[i]>0){
            myfile << endl << "clique constraint " << j+1 << " -> " << rng[i] << endl;
            myfile << "Var    setTo0      setTo1" << endl;
            it = rng[i].getLinearIterator();
            while(it.ok()){
                tmp = it.getVar();
                myfile << tmp ;
                tmp.setUB(IloNum(0));
                if(!cplexR.solve()){
                    myfile << " " <<  -1;
                }else{
                    myfile << (double)cplexR.getObjValue();
                }
                tmp.setUB(IloNum(1));
                tmp.setLB(IloNum(1));
                if(!cplexR.solve()){
                    myfile << " " << -1 << endl;
                }else{
                    myfile << " " << cplexR.getObjValue() << endl;
                }
                tmp.setLB(IloNum(0));
                ++it;  
            }
            j++;
        }
        if(cliques[i]==2){
            it = rng[i].getLinearIterator();
            while(it.ok()){
                it.getVar().setUb(IloNum(0));
                ++it;
            }
            if(!cplexR.solve()){
               it = rng[i].getLinearIterator();
               while(it.ok()){
                  it.getVar().setUb(IloNum(1));
                  ++it;
               }
            }
            myfile << "All Zeroes: " << cplexR.getObjValue() << endl;   
            it = rng[i].getLinearIterator();
            while(it.ok()){
                  it.getVar().setUb(IloNum(1));
                  ++it;
            }
        }
        
    }
   env.end();
   return 0;
}