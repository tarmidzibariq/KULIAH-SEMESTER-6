function transpose(transactions) {
  const itemSets = {};
  transactions.forEach((transaction, tid) => {
    transaction.forEach(item => {
      if (!itemSets[item]) itemSets[item] = new Set();
      itemSets[item].add(tid);
    });
  });
  return itemSets;
}

function eclat(itemSets, minSupport, totalTransactions) {
  const results = [];

  function recursive(prefix, items) {
    for (let [item, tids] of items) {
      const newPrefix = [...prefix, item];
      const support = tids.size / totalTransactions;

      if (support >= minSupport) {
        results.push({ items: newPrefix, support });

        const newItems = new Map();
        for (let [otherItem, otherTids] of items) {
          if (item < otherItem) {
            const intersection = new Set([...tids].filter(x => otherTids.has(x)));
            if (intersection.size / totalTransactions >= minSupport) {
              newItems.set(otherItem, intersection);
            }
          }
        }

        recursive(newPrefix, newItems);
      }
    }
  }

  recursive([], Object.entries(itemSets).map(([k, v]) => [k, v]));
  return results;
}

module.exports = { transpose, eclat };
