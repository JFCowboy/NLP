# -*- coding: cp1252 -*-
# PARA PYTHON 2.7
import lexsim
from scipy.stats.stats import pearsonr

def clean(texto):
    signos_puntuacion=".,;:'()-[]{}#$&/?!"
    for signo_puntuacion in signos_puntuacion:
        texto=texto.replace(signo_puntuacion," ")
    return texto.split()

def leer_dataset_textsim(nombre_archivo):
    path="./data_textsim/"
    dataset=[]
    archivo=open(path+nombre_archivo,"r")
    for linea in archivo.readlines():
        pos_tab=linea.find("\t")
        texto1=clean(linea[:pos_tab])
        texto2=clean(linea[pos_tab+1:-1])
        dataset.append([texto1,texto2])
    archivo.close()
    archivo=open(path+nombre_archivo.replace(".input",".gs"),"r")
    tmp_gs=[]
    for linea in archivo.readlines():
        if linea.strip()!="":
            gs=float(linea)
            tmp_gs.append(gs)
    return (dataset,tmp_gs)


datasets=[
"2012.input.MSRpar.txt",
"2012.input.MSRvid.txt",
"2012.input.OnWN.txt",
"2012.input.SMTeuroparl.txt",
"2012.input.SMTnews.txt",
"2013.input.FNWN.txt",
"2013.input.headlines.txt",
"2013.input.OnWN.txt",
"2013.input.SMT.txt",
"2014.input.deft-forum.txt",
"2014.input.deft-news.txt",
"2014.input.headlines.txt",
"2014.input.images.txt",
"2014.input.OnWN.txt",
"2014.input.tweet-news.txt",
"2015.input.answers-forums.txt",
"2015.input.answers-students.txt",
"2015.input.belief.txt",
"2015.input.headlines.txt",
"2015.input.images.txt",
"2016.input.answer-answer.txt",
"2016.input.headlines.txt",
"2016.input.plagiarism.txt",
"2016.input.postediting.txt",
"2016.input.question-question.txt",
    ]


#####################################################################3
#FUNCIONES DE SIMILITUD TEXTUAL
#####################################################################3
def STS_monge_elkan(texto1,texto2,lexsim):
    suma=0.0
    for palabra1 in texto1:
        maxsim=0
        for palabra2 in texto2:
            sim=lexsim(palabra1,palabra2)
            if sim>maxsim:
                maxsim=sim
        suma+=maxsim
    if len(texto1)==0:
        return 0.0
    return suma/len(texto1)


def GEN_monge_elkan(texto1,texto2,lexsim, m=2):
    suma=0.0
    for palabra1 in texto1:
        maxsim=0
        for palabra2 in texto2:
            sim=lexsim(palabra1,palabra2)
            if sim>maxsim:
                maxsim=sim
        suma+=maxsim**m
    if len(texto1)==0:
        return 0.0
    return (suma/len(texto1))**(1.0/m)



def similitudTextos(simiText, simiLex, m=0): 
    suma_Pearson_r=0.0
    suma_numero_de_pares=0
    suma_Pearson_r_year={"2012":0.0,"2013":0.0,"2014":0.0,"2015":0.0,"2016":0.0}
    suma_numero_de_pares_year={"2012":0,"2013":0,"2014":0,"2015":0,"2016":0}
    print "DATASET\t#pares\tPearson r"
    for dataset in datasets:
        predicciones=[]
        d,gs=leer_dataset_textsim(dataset)
        for texto1,texto2 in d:

            # EJEMPLOS
            #prediccion=STS_monge_elkan(texto1,texto2,lexsim.lex_sim_jaccard)
            #prediccion=GEN_monge_elkan(texto1,texto2,lexsim.lex_sim_jaccard)
            #prediccion=STS_monge_elkan(texto1,texto2,lexsim.lex_sim_Jaro)
            #prediccion=STS_monge_elkan(texto1,texto2,lexsim.lex_sim_path_edit_distance) # ojo, demora much�simo
            #prediccion = STS_monge_elkan(texto1,texto2,lexsim.lex_sim_word2vec)
            if m > 0:
                prediccion = simiText(texto1,texto2,simiLex, m=m)
            else:

                prediccion = simiText(texto1,texto2,simiLex)
            
            predicciones.append(prediccion)
        Pearson_r=pearsonr(gs,predicciones)[0]
        print dataset,"\t",len(d),"\t",round(Pearson_r,4)

        #actualiza el promedio ponderado de todos los datasets
        suma_Pearson_r+=Pearson_r*len(d)
        suma_numero_de_pares+=len(d)
        #actualiza el promedio ponderado por a�o
        for year in suma_Pearson_r_year:
            if year in dataset:
                suma_Pearson_r_year[year]+=Pearson_r*len(d)
                suma_numero_de_pares_year[year]+=len(d)
         

    print "Promedio ponderado todos\t",suma_numero_de_pares,"\t",round(suma_Pearson_r/suma_numero_de_pares,4)

    mejor_en_SemEval={
        "2012":"0.6773 UKP",
        "2013":"0.6181 UMBC",
        "2014":"0.7610 DLS@CU",
        "2015":"0.8015 DLS@CU",
        "2016":"0.7781 Samsung Poland NLP",
        }
    for year in ["2012","2013","2014","2015","2016"]:
        print "Promedio ponderado",year,"\t",suma_numero_de_pares_year[year],"\t",round(suma_Pearson_r_year[year]/suma_numero_de_pares_year[year],4),"\tMejor en SemEval:\t",mejor_en_SemEval[year]


if __name__ == '__main__':  # ESTE "IF" ES PARA QUE LA SIGUIENTE PARTE DEL CODIGO NO SE EJECUTE CUANDO ESTE PROGRAMA SE IMPORTE EN OTRO PROGRAMA CON import textsim
    funciones = [GEN_monge_elkan, STS_monge_elkan]
    #vec_sim_lex = [lexsim.lex_sim_jaccard, lexsim.lex_sim_jaccard_ngrams, lexsim.lex_sim_cosine, lexsim.lex_sim_Jaro, lexsim.lex_sim_edit_distance, lexsim.lex_sim_path, lexsim.lex_sim_lch, lexsim.lex_sim_wup, lexsim.lex_sim_res, lexsim.lex_sim_jcn, lexsim.lex_sim_lin, lexsim.lex_sim_word2vec, lexsim.lex_sim_path_edit_distance, lexsim.lex_sim_path_jaccard_23grams_porter]
    vec_sim_lex = [lexsim.lex_sim_jaccard, lexsim.lex_sim_jaccard_ngrams, lexsim.lex_sim_cosine, lexsim.lex_sim_Jaro, \
                lexsim.lex_sim_path, lexsim.lex_sim_lch, lexsim.lex_sim_wup, lexsim.lex_sim_res, lexsim.lex_sim_jcn,  \
                lexsim.lex_sim_lin, lexsim.lex_sim_word2vec, lexsim.lex_sim_path_jaccard_23grams_porter]
    #vec_sim_lex = [lexsim.lex_sim_jaccard]                
    for fun in funciones:
        for s in vec_sim_lex:
            similitudTextos(fun,s)
            print "---"*5, fun,",",s,"\n";

    for m in xrange(5):
        for s in vec_sim_lex:
            similitudTextos(funciones[0],s, m=m)
            print "---"*5, funciones[0],",",s, " m=", m,"\n";
