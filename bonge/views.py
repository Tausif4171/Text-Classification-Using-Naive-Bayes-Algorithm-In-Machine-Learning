from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import sklearn.datasets as skd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.metrics import accuracy_score


def home(request):
    return render(request, 'bonge/home.html')


def predict(request):
    if request.method == 'POST':
        usertext = request.POST['usertext']
        print("Data received")
        print(usertext)
    else:
        print("No Data received")


    # df = load_and_clean_data()

    # Importing Dataset offline
  

    categories = ['alt.atheism','soc.religion.christian','comp.graphics','sci.med']

    news_train = skd.load_files('C:/Users/sumayya khan/Desktop/Machine Learning/20news-bydate/20news-bydate-train',categories = categories, encoding='ISO-8859-1')

    news_test = skd.load_files('C:/Users/sumayya khan/Desktop/Machine Learning/20news-bydate/20news-bydate-test', categories = categories, encoding='ISO-8859-1')
   

    count_vect = CountVectorizer()
    X_train_tf = count_vect.fit_transform(news_train.data)
    # print(X_train_tf.shape)

    
    # create the transform
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_tf)
    print(X_train_tfidf.shape)

    
    clf = MultinomialNB().fit(X_train_tfidf, news_train.target) # Here we are Training our model

    # The code taken from main.py file.
    # docs_new = ['God is love', 'OpenGL on the GPU is fast', ' God’s love is different from other kinds of love ']
    # username = input("Enter username: ")
    # print("Username is: " + username)
    input=[usertext]

    X_new_counts = count_vect.transform(input)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    predicted = clf.predict(X_new_tfidf)

    for x in predicted:
        print("This will come under in",x,"Category.")
        
    print(news_train.target_names)
    # //end


    X_test_tf = count_vect.transform(news_test.data)
    X_test_tfidf = tfidf_transformer.transform(X_test_tf)
    predicted = clf.predict(X_test_tfidf)

    
    print("Accuracy: ",accuracy_score(news_test.target, predicted))
    print(metrics.classification_report(news_test.target, predicted, target_names = news_test.target_names))
    print(metrics.confusion_matrix(news_test.target, predicted))

    data = x
    if (data==0):
        category = "alt.atheism"
        context1 = {'Result' : category}
    elif (data==1):
        category = "comp.graphics"
        context1 = {'Result' : category}
    elif (data==2):
        category = "sci.med"
        context1 = {'Result' : category}
    elif (data==3):
        category = "soc.religion.christian"
        context1 = {'Result' : category}
    else:
        category = "None"
        context1 = {'Result' : category}

        
    # context1 = {'Result is': data}
    context2 = {'Accuracy' : accuracy_score(news_test.target, predicted)}

    print("Result is: ", context1)

    data = usertext
    context3 = {'Data is': data}


    return render(request, 'bonge/result.html', {'context1': context1, 'context2': context3})


def team(request):
    return render(request, 'bonge/team.html')


def about(request):
  return render(request, 'bonge/about.html')


  