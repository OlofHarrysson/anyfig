module.exports = {
  // docs: {
  //   'Getting Started': ['doc1', 'doc2'],
  //   'Usage': ['doc2'],
  //   'Advanced Usage': ['doc3'],
  // },

  docs: [

    {
      type: 'category',
      label: 'Getting Started',
      items: ['about', 'installation'],
    },

    {
      type: 'category',
      label: 'Usage',
      items: ['fundamentals', 'advanced', 'API'],
    },

    {
      type: 'category',
      label: 'Common Patterns',
      items: ['shadow-configs'],
    },

    {
      type: 'category',
      label: 'Resources',
      items: [
      
        {
          type: 'link',
          label: 'GitHub',
          href: 'https://github.com/OlofHarrysson/anyfig'
        },

        {
          type: 'link',
          label: 'Online Demo',
          href: 'https://pyfiddle.io/fiddle/4de2f70f-e421-4326-bbb8-b06d5efa547d/?i=true',
        },

      ],
    },



 
  ],

};
