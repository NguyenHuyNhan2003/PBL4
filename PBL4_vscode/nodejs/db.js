const Client = require('mongodb').MongoClient;
const Exceljs = require('exceljs');
const express = require('express');
const morgan = require('morgan');
const mongoose = require('mongoose');

const excelPath = "../result/post_text_date.xlsx";
const mongoURI = 'mongodb+srv://nathan:PBL4@pbl4.xemvqhk.mongodb.net/PBL4?retryWrites=true&w=majority';

//connect to mongoDB
mongoose.connect(mongoURI)
.then((result)=> console.log("Connected!"))
.catch((err)=> console.log(err));


