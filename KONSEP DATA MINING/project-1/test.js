const fs = require('fs');
const csv = require('csv-parser');
const FPGrowth = require('node-fpgrowth').FPGrowth;
const Apriori = require('node-apriori');
const { transpose, eclat } = require('./eclat');

const transactions = [];

fs.createReadStream('Retail_Products_Only-2.csv')
  .pipe(csv())
  .on('data', (row) => {
    const items = Object.values(row).filter(Boolean);
    transactions.push(items);
  })
  .on('end', async () => {
    console.log('Dataset loaded.');

    const minSupport = 0.02;

    // FP-Growth
    const fpStart = performance.now();
    const fp = new FPGrowth(minSupport);
    fp.exec(transactions).then(result => {
      const fpEnd = performance.now();
      console.log(`FP-Growth found ${result.length} patterns in ${fpEnd - fpStart} ms`);
    });

    // Apriori
    const aprioriStart = performance.now();
    AprioriApriori = new Apriori.Apriori(minSupport);

    AprioriApriori.on('data', () => {}); // bisa dilepas kalau gak dipakai

    AprioriApriori.exec(transactions).then(result => {
      const aprioriEnd = performance.now();
      console.log(`Apriori found ${result.itemsets.length} patterns in ${aprioriEnd - aprioriStart} ms`);
    });

    // ECLAT
    const eclatStart = performance.now();
    const tidSets = transpose(transactions);
    const eclatResult = eclat(tidSets, minSupport, transactions.length);
    const eclatEnd = performance.now();
    console.log(`ECLAT found ${eclatResult.length} patterns in ${eclatEnd - eclatStart} ms`);
  });
