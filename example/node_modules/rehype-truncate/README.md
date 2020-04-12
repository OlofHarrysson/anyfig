# rehype-truncate

```bash
npm i rehype-truncate
```

## Example

Rehype truncate is a plugin for rehype that lets you truncate a hast.

```js
import unified from "unified";
import html from "rehype-parse";
import rehypeTruncate from "rehype-truncate";
import stringify from "rehype-stringify";

const document = `
  <html>
    <head></head>
    <body>
      <h1>Hello, World.</h1>
      <p>This is an example document to test html truncation.</p>
    </body>
  </html>
`;

const processedDocument = unified()
  .use(html)
  .use(rehypeTruncate, { maxChars: 50 })
  .use(stringify)
  .processSync(document).contents;

console.log(processedDocument);
```

This results in the following:

```html
<html>
  <head></head>
  <body>
    <h1>Hello, World.</h1>
    <p>This is an example…</p>
  </body>
</html>
```

## Ignoring tags

You can configure `rehype-truncate` to ignore content inside certain tag names by using the `ignoreTags` options.

```js
import unified from "unified";
import html from "rehype-parse";
import rehypeTruncate from "rehype-truncate";
import stringify from "rehype-stringify";

const document = `
  <html>
    <head></head>
    <body>
      <h1>Hello, World.</h1>
      <p>This is an example document to test html truncation.</p>
      <ul>
        <li>List item 1</li>
        <li>List item 2</li>
        <li>List item 3</li>
        <li>List item 4</li>
      </ul>
      <p>This example has a list that should get ignored by the truncation character count.</p>
    </body>
  </html>
`;

const processedDocument = unified()
  .use(html)
  .use(rehypeTruncate, { maxChars: 120, ignoreTags: ["ul"] })
  .use(stringify)
  .processSync(document).contents;

console.log(processedDocument);
```

This results in the following:

```html
<html>
  <head></head>
  <body>
    <h1>Hello, World.</h1>
    <p>This is an example document to test html truncation.</p>
    <ul>
      <li>List item 1</li>
      <li>List item 2</li>
      <li>List item 3</li>
      <li>List item 4</li>
    </ul>
    <p>This example has a lis…</p>
  </body>
</html>
```

## Options

| Name         | Type        | Description                                       |
| ------------ | ----------- | ------------------------------------------------- |
| `maxChars`   | `number`    | The number of characters to truncate.             |
| `ignoreTags` | `string[]?` | Ignore contents of certain tag names.             |
| `disable`    | `boolean?`  | Disable truncation and return the document as is. |
