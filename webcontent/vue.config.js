module.exports = {
    publicPath: '/',
    outputDir: 'dist',
    assetsDir: "assets",
    productionSourceMap: false,
    filenameHashing: false,
    lintOnSave: true,
    devServer: {
        open: false,
        host: '0.0.0.0',
        port: 8070,
        https: false,
        hotOnly: false,
        disableHostCheck: true,
        proxy:{
            '/sys/api': {
                target: 'http://10.10.10.130:8000/',
                changeOrigin: true,
                secure:false
            },
            '/asset/api': {
                target: 'http://10.10.10.130:8001/',
                changeOrigin: true,
                secure:false
            },
            '/monitor/api': {
                target: 'http://10.10.10.130:8002/',
                changeOrigin: true,
                secure:false
            },
            '/automation/api': {
                target: 'http://localhost:8003/',
                changeOrigin: true,
                secure:false
            },
            '/phy_topo': {
                target: 'http://10.230.13.41:5000/',
                changeOrigin: true,
                secure:false
            }
        }
    }

}
