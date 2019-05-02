module.exports = {
    root: true,
    env: {
      node: true
    },
    'extends': [
      'plugin:vue/essential',
      // '@vue/prettier'
    ],
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',

      // allow paren-less arrow functions
      'indent': ["warn", 4, { "CallExpression": {"arguments":"off"}}],
      'semi': ["warn", "always"],
      'space-before-blocks': 0,
      'space-before-function-paren': 0,
      'padded-blocks': 0,
      'quotes': 0,
      'no-multiple-empty-lines': 0,
      'arrow-parens': 0,
      'one-var': 0,
      // 'import/first': 0,
      // 'import/named': 2,
      // 'import/namespace': 2,
      // 'import/default': 2,
      // 'import/export': 2,
      // allow debugger during development
      'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
      // 'brace-style': ["warn", "allman"],
      // 'keyword-spacing': ["warn", { "overrides": { "if": { "after": false }, "for": { "after": false }, "while": { "after": false } } }],
      'no-unused-vars': ["warn"],
      'no-useless-escape': 0,
      'camelcase': 0,
      'spaced-comment': 0,
      // 'brace-style': [2, 'stroustrup', { 'allowSingleLine': true }]
    },
    parserOptions: {
      parser: 'babel-eslint'
    }
  }
