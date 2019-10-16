module.exports = {
    verbose: true,
    moduleFileExtensions: [
        "js",
        "json",
        "vue"
    ],
    transform: {
        ".*\\.(vue)$": "vue-jest",
        "^.+\\.js$": "babel-jest"
    },
    collectCoverage: false,
    collectCoverageFrom: [
        "src/components/*.{js,vue}",
        "!**/node_modules/**"
    ],
    coverageReporters: [
        "html",
        "text-summary"
    ],
    transformIgnorePatterns: ["/node_modules/"]
    // "transformIgnorePatterns": [
    //     "node_modules/(?!@ngrx|(?!deck.gl)|ng-dynamic)"
    //   ]
}

// module.exports = {
//     moduleFileExtensions: ["js", "jsx", "json", "vue"],
//     transform: {
//         "^.+\\.vue$": "vue-jest",
//         ".+\\.(css|styl|less|sass|scss|svg|png|jpg|ttf|woff|woff2)$": "jest-transform-stub",
//         "^.+\\.jsx?$": "babel-jest"
//     },
//     transformIgnorePatterns: ["/node_modules/"],
//     moduleNameMapper: {
//         "^@/(.*)$": "<rootDir>/src/$1"
//     },
//     snapshotSerializers: ["jest-serializer-vue"],
//     // testMatch: ["**/tests/unit/**/*.spec.(js|jsx|ts|tsx)|**/__tests__/*.(js|jsx|ts|tsx)"],
//     testURL: "http://localhost/",
//     watchPlugins: ["jest-watch-typeahead/filename", "jest-watch-typeahead/testname"]
// };
