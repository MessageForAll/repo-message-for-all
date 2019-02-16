'use strict';

const app = require('../src/app');
const debug = require('debug')('nodestr:server');
const http = require('http');

const port = normalizePort(process.env.PORT || '3001');
app.set('port', port);
const server = http.createServer(app);

//--------------------- Server ----------------------//
server.listen(port,() => {
    // Para mostrar no prompt
    console.log('API rodando na porta', port);
});

// Inserir as funcoes desejadas amarradas para cada tipo de evento
server.on('error', onError);
server.on('listening', onListening)

//---------------------- Funcoes ---------------------//
function normalizePort(val) {
    const port = parseInt(val, 10)
    if (isNaN(port)) {
        return val;
    }
    if (port > 0) {
        return port
    }
    return false;
};

function onError(error) {
    if (error.syscall !== 'listem') {
        throw error;
    }

    const bind = typeof port == 'string'// se (typeof(port) == 'string') entao(?) .. senao(:)
        ? 'Pipe ' + port
        : 'Port ' + port;

    switch (error.code) {
        case 'EACCES':
            console.error(bind + ' requires elevated privileges');
            process.exit(1);
            break;
        case 'EADDRINUSE':
            console.error(bind + ' is already in use');
            process.exit(1);
            break;
        default:
            throw error;
    }
};

function onListening() {
    const addr = server.address();
    const bind = typeof (addr) === 'string'
        ? 'Pipe ' + addr
        : 'Port ' + addr.port;
    debug('Listening on ' + bind);
};