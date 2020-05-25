module.exports = {
  themes: [
    '@docusaurus/theme-search-algolia',
    '@docusaurus/plugin-google-analytics',
    '@docusaurus/plugin-sitemap',
    {
      cacheTime: 600 * 1000, // 600 sec - cache purge period
      changefreq: 'weekly',
      priority: 0.5,
    },
  ],

  title: 'Anyfig',
  tagline: 'Anything in your configs',
  url: 'https://your-docusaurus-test-site.com',
  baseUrl: '/',
  favicon: 'img/favicon.ico',
  organizationName: 'OlofHarrysson', // Usually your GitHub org/user name.
  projectName: 'Anyfig', // Usually your repo name.
  themeConfig: {
    sidebarCollapsible: false,

    // Google Analytics
    googleAnalytics: {
      trackingID: 'UA-163686450-1',
      anonymizeIP: true,
    },

    // Search
    algolia: {
      appId: 'BH4D9OD16A',
      apiKey: '2482404787a69df7a47eeb3e31da3212',
      indexName: 'anyfig',
      algoliaOptions: {}, // Optional, if provided by Algolia
    },

    // Syntax color theme
    prism: {
      // theme: require('prism-react-renderer/themes/oceanicNext'),
      theme: require('prism-react-renderer/themes/vsDark'),
    },

    navbar: {
      title: 'Anyfig',
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.svg',
      },

      links: [{
        to: 'docs/introduction',
        activeBasePath: 'docs',
        label: 'Docs',
        position: 'left',
      },
      {
        href: 'https://github.com/OlofHarrysson/anyfig',
        label: 'GitHub',
      },
      {
        href: 'https://pyfiddle.io/fiddle/4de2f70f-e421-4326-bbb8-b06d5efa547d/?i=true',
        label: 'Online Playground',
      },
      ],
    },
    footer: {
      style: 'dark',
      links: [{
        title: 'Docs',
        items: [{
          label: 'Style Guide',
          to: 'docs/doc1',
        },
        {
          label: 'Second Doc',
          to: 'docs/doc2',
        },
        ],
      },
      {
        title: 'Community',
        items: [{
          label: 'Stack Overflow',
          href: 'https://stackoverflow.com/questions/tagged/docusaurus',
        },
        {
          label: 'Discord',
          href: 'https://discordapp.com/invite/docusaurus',
        },
        ],
      },
      {
        title: 'Social',
        items: [{
          label: 'Blog',
          to: 'blog',
        },
        {
          label: 'GitHub',
          href: 'https://github.com/facebook/docusaurus',
        },
        {
          label: 'Twitter',
          href: 'https://twitter.com/docusaurus',
        },
        ],
      },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
    },

  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          // routeBasePath: '',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/facebook/docusaurus/edit/master/website/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};