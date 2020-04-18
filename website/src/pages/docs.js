import React from 'react';

import {Redirect} from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';

// Redirects to docs-page
function Docs() {
  return <Redirect to={useBaseUrl('/docs/introduction')} />;
}

export default Docs;
