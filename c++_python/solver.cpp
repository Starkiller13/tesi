#include<iostream>
#include<fstream>
#include<strings.h>
#include <ilcplex/cplex.h>
#include <ilcplex/ilocplex.h>
ILOSTLBEGIN

char * f = (char *) malloc(1000);
int i,j,clique_counter,lp_counter,min_eq_counter;
bool isClique = true;

int main(int argc, char **argv){
   IloEnv env;
   IloInt temp;
   IloModel model(env);
   IloModel modelRelaxed(env);
   IloObjective obj;
   IloNumVarArray var(env);
   IloRangeArray rng(env);
   IloCplex cplex(model);
   IloNumArray u_res(env);
   IloNumArray l_res(env);
   IloNumArray rng_res(env);
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
   
   /*array in cui salvo la posizione delle variabili
     booleane a modo di bucket*/
   int boolvars[var.getSize()];
   for(i = 0;i < var.getSize(); i++){
      boolvars[i] = 0;
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
               min_eq_counter++;
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

   /*Salvo la posizione di tutte le variabili boolean*/
   for(i = 0;i < var.getSize(); i++){
      if(var[i].getType()==IloNumVar::Type::Bool){
         boolvars[i] = 1;
         lp_counter += 2;
      }
   }
   modelRelaxed.add(rng);
   modelRelaxed.add(obj);
   for(i = 0;i < var.getSize();i++){
      modelRelaxed.add(IloConversion(env,var[i],ILOFLOAT));
   }
   IloCplex cplexR(modelRelaxed);
   cplexR.setParam(IloCplex::PreInd, false);
   /*Per info salvo il numero di rilassamenti che dovrò fare*/
   lp_counter += min_eq_counter;
   /*Risolvo il rilassaento senza modifiche*/
   try{
      if(!cplexR.solve()){
         cerr << "Something went wrong" << endl;
         return 1;
      }
      ref = cplexR.getObjValue();
      cout << ref;
   }catch(IloException& e){
      cout << e << endl;
   }
   /*Risolvo 2 rilassamenti a variabile impostandola
     inizialmnte a 1 e in seguito a 0*/
   j=1;
   for(i = 0;i < var.getSize(); i++){
      if(boolvars[i]!=0){
         /*Fisso una variabile a 1 cambiando
           il suo lower bound*/
         var[i].setLb(IloNum(1));
         try{
            cout << endl << "----LP " << j << "/" << lp_counter << " -----"<< endl << endl;
            if(!cplexR.solve()){
               var[i].setLb(IloNum(0));
               cerr << "no solution" << endl;
               u_res.add(IloNum(-1));
            }
            u_res.add(cplexR.getObjValue());   
         }catch(IloException& f){
            cout << "IloException : " << f << endl;
         }catch(...){
            cout << "Generic Exception" << endl;
         }
         /*Ripristino il lower bound*/
         var[i].setLb(IloNum(0));
         j++;

         /*Fisso una variabile a 0 cambiando 
           il suo upper bound*/
         var[i].setUb(IloNum(0));
         try{
            cout << endl << "----LP " << j << "/" << lp_counter << " -----"<< endl << endl;
            if(!cplexR.solve()){
               var[i].setUb(IloNum(1));
               cerr << "no solution" << endl;
               l_res.add(IloNum(-1));
            }
            l_res.add(cplexR.getObjValue());
         }catch(IloException& f){
            cout << "IloException : " << f << endl;
         }catch(...){
            cout << "Generic Exception" << endl;
         }
         /*Ripristino l'upper bound*/
         var[i].setUb(IloNum(1));
         j++;
      }else{
         l_res.add(IloNum(NULL));
         u_res.add(IloNum(NULL));
      }
   }
   /*Se il vincolo è di <= risolvo il rilassamento impostand
     tutte le varibili del vincolo a 0*/
   for(i = 0; i < rng.getSize(); i++){
      if(cliques[i]==2){
         it = rng[i].getLinearIterator();
         while(it.ok()){
            it.getVar().setUb(IloNum(0));
            ++it;
         }
         cout << endl << "----LP " << j << "/" << lp_counter << " -----"<< endl << endl;
         try{
            if(!cplexR.solve()){
               it = rng[i].getLinearIterator();
               while(it.ok()){
                  it.getVar().setUb(IloNum(1));
                  ++it;
               }
               rng_res.add(IloNum(-1));
            }
            rng_res.add(cplexR.getObjValue());   
         }catch(IloException& f){
            cout << "IloException : " << f << endl;
         }catch(...){
            cout << "Generic Exception" << endl;
         }
         it = rng[i].getLinearIterator();
         while(it.ok()){
            it.getVar().setUb(IloNum(1));
            ++it;
         }
         j++;
      }
   }

   /*Gestisco la raccolta dei dati salvandoli in un file*/
   myfile << "MIP: " << argv[1] << endl;
   myfile << "LP relaxation result: " << ref << endl << endl; 
   j = 0;
   for(i = 0; i < rng.getSize(); i++){
      if(cliques[i]==2){
         myfile << endl << "clique constraint " << j+1 << " -> " << rng[i] << endl;
         myfile << "Var    setTo0      setTo1" << endl;
         it = rng[i].getLinearIterator();
         while(it.ok()){
            temp = var.find(it.getVar());
            myfile << var[temp] << " " << l_res[temp] << " " << u_res[temp] << endl;
            ++it;
         }
         myfile << "All Zeroes: " << rng_res[j] << endl;
         j++;
      }else if(cliques[i]==1){
         myfile << endl << "clique constraint " << j+1 << " -> " << rng[i] << endl;
         myfile << "Var    setTo0      setTo1" << endl;
         it = rng[i].getLinearIterator();
         while(it.ok()){
            temp = var.find(it.getVar());
            myfile << var[temp] << " " << l_res[temp] << " " << u_res[temp] << endl;
            ++it;
         }
         j++;
      }
   }
   env.end();
   return 0;
}