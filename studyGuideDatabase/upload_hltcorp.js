const sqlitemongo = require('../node_modules/sqlitemongo');

async function test() {
	var sqlitePath = '';
	var mongoURI = '';
	var mongoDbName = '';
	await sqlitemongo(sqlitePath, mongoURI, mongoDbName /* optional */);
}
console.log('Starting...');
test().catch(console.error);
console.log('Done.');
