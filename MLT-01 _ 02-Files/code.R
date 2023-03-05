library(flexclust) # for kcca
library(arm) # for bayesglm
library(randomForest) # for RF
library(caret)
library(gbm)
library(splines)
library(parallel)
library(glm)
library(MASS)
library(e1071)
library(glmnet)





data = read.csv("data.csv",header=TRUE,stringsAsFactors = FALSE)

traindata= data[1:500,]

testdata = data[501:1000,]

lrmodel = glm(target~.,data=traindata[,-1],family=binomial)

summary(lrmodel)


testdata$lrprob = predict(lrmodel,type="response",newdata = testdata)
testdata$lrprob=ifelse(testdata$lrprob>.5,1,0)
write.csv(testdata,"result.csv")

table(testdata$lrprob,testdata$target)


#**********************************************************LDA*************************************


ldamodel = lda(target~.,data=traindata[,-1],family=binomial)
lda.pred=predict(ldamodel,testdata)
testdata$ldaprob=lda.pred$posterior[,1]
ldamodel




qdamodel = qda(target~.,data=traindata[,-1],family=binomial)
qda.pred=predict(qdamodel,testdata)
testdata$qdaprob=lda.pred$posterior[,1]



#****************************************************GBM*********************************************

bag.pivot =gbm(target~.,traindata[,-1],distribution = "bernoulli",n.trees=200,interaction.depth = 3,shrinkage = .01)
pnL_prob=predict(bag.pivot,type="response",newdata = testdata[,-1],n.trees=200)  
testdata$gbmprobs = pnL_prob


#******************************************************************RF **********************************

bag.pivot=randomForest(target~.,data=traindata[,-1],mtry=2,importance=TRUE,ntree=500)

pnL_prob=predict(bag.pivot,type="prob",newdata = testdata[,-1])

testdata$rf= pnL_prob[,2]




#***********************************************************SVM
traindata$target=as.factor(traindata$target)
svmfit= svm(target~.,data=traindata[,-1],kernel="linear",scale=TRUE,cost=10,probability = TRUE)
svmfit$index
tune.out=tune(svm,train.x=traindata[,c(2:13)],train.y = traindata[,14],kernel="linear",ranges=list(cost=c(.1,1,10)))
summary(tune.out)
svmfit=tune.out$best.model
svmpred = predict(svmfit,testdata[,c(2:13)],probability=TRUE)
testdata$svmprobs = attr(svmpred, "probabilities")



svmfit= svm(target~.,data=traindata[,-1],kernel="linear",scale=TRUE,cost=1,gamma=1,probability = TRUE)
svmpred = predict(svmfit,testdata[,c(2:13)],probability=TRUE)
testdata$svmprobs = attr(svmpred, "probabilities")
tune.out=tune(svm,train.x=traindata[,c(2:13)],train.y = traindata[,14],kernel="linear",ranges=list(cost=c(.1,1,10),gamma=c(.5,1)))





#*****************************************************************RIDGE***************************************



grid=10^seq(10,-2,length=10)
data = read.csv("IT_training.csv",header=TRUE,stringsAsFactors = FALSE)

traindata= data[1:1200,]

testdata = data[1201:1400,]
x=as.matrix(traindata[,c(12:727)])
y = traindata$X.1_Target

xtest=as.matrix(testdata[,c(12:727)])
ytest = testdata$X.1_Target



#alpha = 0 ridge
#alpha = 1 lasso 
ridge.mod = glmnet(x,y,alpha=0,lambda=grid)
dim(coef(ridge.mod))
# l2 norm of coefficient 
ridge.mod$lambda[1] 
coef(ridge.mod)[,10]
sqrt(sum(coef(ridge.mod)[ -1 ,10]^2) )

ridge.pred=predict(ridge.mod,s=4,newx=xtest)

cv.out =cv.glmnet (x ,y ,alpha =0)
bestlam =cv.out$lambda.min


ridge.pred=predict(ridge.mod,s=bestlam,newx=xtest)

testdata$ridge = ridge.pred
write.csv(testdata,"t.csv")
