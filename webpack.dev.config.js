require('dotenv').config()

const { merge } = require('webpack-merge')
const path = require('path')
const common = require('./webpack.common.config')

const { PORT, CLIENT_PORT } = process.env

const config = {
  mode: 'development',
  optimization: {
    usedExports: true,
    moduleIds: 'named',
    chunkIds: 'named'
  },
  devtool: 'eval-source-map',
  stats: {
    moduleAssets: false,
  },
  devServer: {
    hot: true,
    static: {
      directory: path.join(__dirname, 'build'),
      watch: true,
    },
    port: CLIENT_PORT,
    host: 'localhost',
    proxy: {
      target: `http://localhost:${PORT}`,
      context: ['/api', '/socket.io'],
      ws: true,
    },
    webSocketServer: 'ws',
    historyApiFallback: true,
    client: {
      webSocketTransport: 'ws',
      overlay: {
        warnings: false,
        errors: true,
      },
    },
  },
}

module.exports = merge(common, config)
