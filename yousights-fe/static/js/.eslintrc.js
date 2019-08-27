module.exports = {
  env: {
    'node': true,
    'browser': false,
    'es6': true,
  },
  extends: [
    'airbnb-base',
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  rules: {
    "no-console" : "off",
    "linebreak-style": ["error", "unix"],
    "quote-props": "off",
    "prefer-arrow-callback": "off",
    "arrow-parens" : "off",
    "no-shadow" : "off",
    "wrap-iife" : ["error", "inside"],
    "no-undef" : "off",
    "no-loop-func" : "off",
    "func-names" : ["error", "never"],
    "object-shorthand": ["error", "never"],
    "no-plusplus" : [
		"error", 
		{
			"allowForLoopAfterthoughts": true 
		}
  ],
  'max-len': [
    'error',
    120,
    4
  ]
  }
}
