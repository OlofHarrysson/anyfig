module.exports = {
  themes: ['@docusaurus/theme-search-algolia', '@docusaurus/theme-live-codeblock'],
  title: 'Anyfig',
  tagline: 'Anything in your configs',
  url: 'https://your-docusaurus-test-site.com',
  baseUrl: '/',
  favicon: 'img/favicon.ico',
  organizationName: 'OlofHarrysson', // Usually your GitHub org/user name.
  projectName: 'Anyfig', // Usually your repo name.
  themeConfig: {
    sidebarCollapsible: false,

    // Syntax color theme
    // prism: {
    //   // theme: require('prism-react-renderer/themes/oceanicNext'),
    //   theme: require('prism-react-renderer/themes/vsDark'),
    // },
    navbar: {
      title: 'Anyfig',
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.svg',
      },
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
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
          items: [
            {
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
          items: [
            {
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

    algolia: {
      appId: 'F5AH3JU99B',
      apiKey: '2482404787a69df7a47eeb3e31da3212',
      indexName: 'anyfig',
      algoliaOptions: {}, // Optional, if provided by Algolia
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          routeBasePath: '',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/facebook/docusaurus/edit/master/website/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
