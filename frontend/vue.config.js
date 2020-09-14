var ensoConfig = require ('../conf/frontend.config.json');

module.exports = {
    lintOnSave: false,
    // baseUrl: "/dashboard/",
    publicPath: ensoConfig.public_path,
    outputDir: undefined,
    assetsDir: 'assets',
    runtimeCompiler: undefined,
    productionSourceMap: false,
    parallel: false,
    css: undefined,
    configureWebpack: {
        devServer: {
            watchOptions: {
                ignored: /node_modules/,
                poll: 1000
            }
        }
    }
};
