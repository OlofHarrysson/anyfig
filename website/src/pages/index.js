import React from 'react';
import classnames from 'classnames';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';


function Home() {
  const context = useDocusaurusContext();
  const { siteConfig: { customFields = {}, tagline } = {} } = context;

  return (
    <Layout
      permalink="/"
      title={tagline}
      description={customFields.description}>
      <main>
        <div className={styles.hero}>

          <div className={styles.heroInner}>

            {/* Left */}
            <div className={styles.heroLeft}>
              <div>
                <h1 className={styles.heroProjectTitle}>Anyfig</h1>
                <br></br>
                <h1 className={styles.heroProjectTagline}>
                  Create{' '}
                  <span className={styles.heroProjectKeywords}>modular</span>{' '}
                  and{' '}
                  <span className={styles.heroProjectKeywords}>flexible</span>{' '}
                  <span className={styles.heroProjectKeywordsAlt}>configurations</span>{' '}
                  in Python{' '}
                </h1>

                {/* Get Started Button */}
                <div className={styles.indexCtas}>
                  <Link
                    className={styles.indexCtasGetStartedButton}
                    to={useBaseUrl('docs/')}>
                    Get Started
                  </Link>

                  {/* GitHub stars */}
                  <span className={styles.indexCtasGitHubButtonWrapper}>
                    <iframe
                      className={styles.indexCtasGitHubButton}
                      src="https://ghbtns.com/github-btn.html?user=olofharrysson&amp;repo=anyfig&amp;type=star&amp;count=true&amp;size=large"
                      width={140}
                      height={30}
                      title="GitHub Stars"
                    />
                  </span>
                </div>
              </div>
            </div>

            {/* Right */}
            <div className={styles.heroRight}>
              <div className={styles.heroLogo}><img src="img/logo.svg" /></div>
            </div>
            {/* Right End */}

          </div>
        </div>
      </main>
    </Layout >
  );
}

export default Home;
