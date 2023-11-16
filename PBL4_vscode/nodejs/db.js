const Client = require('mongodb').MongoClient;
const Exceljs = require('exceljs');

const excelPath = "./result/post_text_date.xlsx";
const mongoURI = 'mongodb+srv://adminPBL4:admin@pbl4.xemvqhk.mongodb.net/PBL4?retryWrites=true&w=majority';

//connect to mongoDB
Client.connect(mongoURI)
.then( async(client)=> {
        console.log('Connected!')
        const db = client.db("PBL4");

        const workbook = new Exceljs.Workbook();
        await workbook.xlsx.readFile(excelPath);

        const worksheet = workbook.getWorksheet(1);

        const data = [];
        worksheet.eachRow({ includeEmpty: false }, (row, rowNumber) => {
        //the first row contains headers
        if (rowNumber !== 1) {
            const rowData = {};
            row.eachCell((cell, colNumber) => {
            //use column headers as keys
            rowData[worksheet.getRow(1).getCell(colNumber).value] = cell.value;
            });
            data.push(rowData);
        }
        });
        //insert data
        await db.collection('Facebook_Posts').deleteMany();
        //await db.collection('Facebook_Posts').insertMany(data);

        console.log('Inserted!');

        //close connection
        await client.close();
        console.log('Connection closed!');
}).catch((err)=> console.log(err));


