# TapSearch


## What is TapSearch?

TapSearch is a search engine which index documents and searches for top 10 documents in the collection

1) It takes in multiple paragraphs of text, assigns a unique ID To each paragraph and stores the words to paragraph mappings on an inverted index. This is similar to what elasticsearch does.
2) Given a word to search for, it lists out the top 10 paragraphs in which the word is present.


## [Deployment link](http://35.200.180.190/index)

## Features:

1) Add paragraphs.
2) Search for words in the paragraphs.
3) Check the paragraphs & words added which are to be searched.


## How to use:

1) Go to the [deployed link](http://35.200.180.190/index).
2) The [home page](http://35.200.180.190/index) is the index page which contains a textarea to type the paragraphs
3) The [search page](http://35.200.180.190/search) contains a search box after typing the word click on submit, if there is any the top 10 documents are outputted with unique id and theire respective bm25 score.
4) The [clear page](http://35.200.189.190/clear) has a button to clear all the documents indexed.


## How to run:

```
$ git clone https://github.com/Cool-fire/tapsearch
$ cd tapsearch
$ docker-compose up
```

## Scope / Vision of TapSearch:
I would implement several other features to this application like searching an incomplete word and showing relevant documents. I will also take this project to another level by implementing image search by using ML techniques by extracting the text from the image and searching for that information in the indexed documents.

## Sample Inputs & Outputs:

#### Sample Input:
Eight million is the size of the population in Switzerland. Eight million is the number of Indians who wanted to go to last week’s local cricket match in a village out in the countryside, but couldn’t get tickets 

\n\n

Indian food is an inspiration to the world. Swiss food is an inspiration to itself 

\n\n

Switzerland is rich despite an official poverty rate of 8%. India has riches, including an 8% yearly growth potential which is currently held back by unattended poverty.

#### Sample search

###### Input -switzerland

Results: Paragraph 1 and 3 are returned

###### Input - food

Results: Paragraph 2

