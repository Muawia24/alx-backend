import { express } from 'express';
import { createClient } from 'redis';


const listProducts = [
	{id: 1, name: 'Suitcase 250', price: 50, stock: 4},
	{id: 2, name: 'Suitcase 450', price: 100, stock: 10},
	{id: 3, name: 'Suitcase 650', price: 350, stock: 2},
	{id: 4, name: 'Suitcase 1050', price: 550, stock: 5}
  ];

function getItemById(id) {
  return listProducts.find((product) => product.id === id);
}

// Redis server

const client = createClient();

client.on('error', (error) => {
  console.log(`Redis client not connected to server ${error.message}`);
});


function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId){
  const reservedStock = await client.get(`item.${itemId}`);

  return reservedStock;
}

// Routing 

const port = 1245;
const app = express();

app.get('/list_products', (req, res) => {
  res.send(listProducts.map((product) => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
  })));
});

app.get('/list_products/:itemId', (req, res) => {
  const itemId = req.params.itemId;
  const product = getItemById(Number(itemId));

  if (!product) {
    res.status(404).send({"status":"Product not found"})
  } else {
    const reserveStock = await getCurrentReservedStockById(product.id);
    res.send({
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
      currentQuantity: reserveStock === null ? product.stock : Number(reserveStock),
    });
  }
});

app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = req.params.itemId;
  const product = getItemById(Number(itemId));
  if (!product) {
    res.status(404).send({"status":"Product not found"});
    return;
  }
  let reserveStock = await getCurrentReservedStockById(product.id);
  reserveStock = reserveStock === null ? product.stock : Number(reserveStock);
  if (!reserveStock) {
    res.send({"status":"Not enough stock available","itemId":product.id});
  } else {
    reserveStockById(product.id, reserveStock.stock - 1);
    res.send({"status":"Reservation confirmed","itemId":product.id});
  }
});

// Start the server

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
});
