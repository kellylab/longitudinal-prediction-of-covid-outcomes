%% load data
clear all
T=readtable('eap.csv');

M=[];
for p=1:size(T,1)
    for c= 1:size(T,2)
        if iscell(T{p,c})
            tmp=T{p,c};
            if strcmp(tmp{:},'na') || strcmp(tmp{:},'')
                M(p,c)=NaN;
            elseif strcmp(tmp{:},'no') || strcmp(tmp{:},'No') || strcmp(tmp{:},'0')
                M(p,c)=0;
            elseif strcmp(tmp{:},'yes') || strcmp(tmp{:},'Yes') || strcmp(tmp{:},'1')
                M(p,c)=1;
            else
                M(p,c)=NaN;
            end
        elseif isdatetime(T{p,c}) %********** remove all dates from predictors ***********%
            M(p,c)= NaN; %year(T{p,c})*365 + month(T{p,c})*30 + day(T{p,c});
        else
            M(p,c)=T{p,c};
        end
    end
end

%% choose what you want to predict, and which predictors to remove
indRemove=[];
for c= 1:size(T,2)
    if sum(strcmp(T.Properties.VariableNames{c},{'whoscale14','day14_status','discharge_date','mrn','Var1'}))%,'patient_eap_id'})) 
       indRemove = [indRemove c];
    end
    if strcmp(T.Properties.VariableNames{c},'death_date') %I will predict dead/alive
       indY = c;
    end
end
Xall=M;
Xall(:,[indY indRemove])=NaN;

%% multilayer network, few predictors, ablation analysis
th=3;
indpred = (sum(isnan(Xall),1)) < th;
INDPRED=find(indpred);
PredNames = T.Properties.VariableNames(INDPRED);
INDPAT = find((sum(isnan(Xall(:,INDPRED)),2)) == 0);
X = Xall(INDPAT,INDPRED)'; %Matlab required format, dimensions x xsamples
Y=isfinite(M(INDPAT,indY))';
Npatients = numel(INDPAT);
Npredictors = numel(INDPRED);
PropDeaths = sum(Y)/numel(Y);

Nneurons = [50]; % a vector of #neurons in each hidden layer
trainRatio = .9;
valRatio = .1;
testRatio = 0;

nboot = 50;
Performance=NaN(Npredictors+1,nboot);
parfor s=1:nboot %********************************************* all predictors
    tic
    net = patternnet(Nneurons);
    net.divideParam.trainRatio = trainRatio;
    net.divideParam.valRatio = valRatio;
    net.divideParam.testRatio = testRatio;
    net.trainParam.showWindow = false;
    Yval=[];
    for p=1:numel(Y) % cross-validate, leave-one-out
        [net,tr] = train(net,X(:,[1:p-1 p+1:end]),Y([1:p-1 p+1:end]));
        Yval(p) = net(X(:,p));
        %**** use code below for logistic regression instead ***********%
        %b=glmfit(X(:,[1:p-1 p+1:end])',Y([1:p-1 p+1:end])','binomial','link','probit');
        %Yval(p) = glmval(b,X(:,p)','probit');
    end
%     plotperform(tr)
    Performance(1,s) = sum(abs(Y-Yval))/numel(Y);
    toc
end %**********************************************************************
nanmedian(Performance(1,:),2)

parfor a=1:numel(PredNames) %****************************** remove 1 predictor
    indAblate = NaN;
    for c= 1:numel(INDPRED)
        if sum(strcmp(T.Properties.VariableNames{INDPRED(c)},PredNames{a}))
            indAblate = c;
            break;
        end
    end
    X = Xall(INDPAT,INDPRED([1:(indAblate-1) (indAblate+1):end]))';
    for s=1:nboot
        net = patternnet(Nneurons);
        net.divideParam.trainRatio = trainRatio;
        net.divideParam.valRatio = valRatio;
        net.divideParam.testRatio = testRatio;
        net.trainParam.showWindow = false;
        Yval=[];
        for p=1:numel(Y) % cross-validate, leave-one-out
            [net,tr] = train(net,X(:,[1:p-1 p+1:end]),Y([1:p-1 p+1:end]));
            Yval(p) = net(X(:,p));
        end
        Performance(a+1,s) = sum(abs(Y-Yval))/numel(Y);
    end
end %**********************************************************************

figure; hold on
ci=bootci(1000,{@nanmedian,Performance(1,:)},'alpha',0.05);
myerrorbar(1:numel(INDPRED),nanmedian(Performa
nce(1,:),2)*ones(numel(INDPRED),1),(ci*ones(1,numel(INDPRED)))',[.5 .5 .5],1);
ci=bootci(1000,{@nanmedian,Performance(2:end,:)'},'alpha',0.05);
myerrorbar(1:numel(INDPRED),nanmedian(Performance(2:end,:),2),ci','r');
plot(1:numel(INDPRED),PropDeaths*ones(numel(INDPRED),1),'--k');
plot(1:numel(INDPRED),nanmedian(Performance(1,:),2)*ones(numel(INDPRED),1),'--b');
plot(1:numel(INDPRED),nanmedian(Performance(2:end,:),2),'-r');
T.Properties.VariableNames{INDPRED}

%% multilayer network
Performance=[];
Npatients=[];
Npredictors=[];
PropDeaths=[];

parfor th=1:30
    %*** look for complete subsets of the data matrix
    indpred = (sum(isnan(Xall),1)) < th;
    Xred = Xall(:,indpred);
    if th==4
        INDPRED=find(indpred);
    end
    indpat = (sum(isnan(Xred),2)) == 0;
    X = Xred(indpat,:);
    Y=isfinite(M(indpat,indY));
    %*************
    
    X=X';
    Y=Y';
    net = patternnet(5);
    net.divideParam.trainRatio = 80/100;
    net.divideParam.valRatio = 10/100;
    net.divideParam.testRatio = 10/100;
    net.trainParam.showWindow = false;
    Yval=[];
    for p=1:numel(Y)
        [net,tr] = train(net,X(:,[1:p-1 p+1:end]),Y([1:p-1 p+1:end]));
        Yval(p) = net(X(:,p));
    end
    Performance(th) = sum(abs(Y-Yval))/numel(Y);
    Npatients(th) = numel(Y);
    Npredictors(th) = size(X,1);
    PropDeaths(th) = sum(Y)/numel(Y);
end

figure; 
subplot(1,2,1); hold on; axis square; title(T.Properties.VariableNames{indY})
plot(Performance,'-'); ylabel('Classif. Error | Prop. Deaths'); xlabel('Subset rank');
plot(PropDeaths,'--k'); legend({'Classif. Error','Prop. Deaths'})
subplot(1,2,2); hold on; axis square
plot(Npatients,'-r');plot(Npredictors,'-b');
legend({'N patients','N predictors'})
ylabel('N'); xlabel('Subset rank');


T.Properties.VariableNames{INDPRED}

%%




















%%
