---
name: nextjs-optimization
description: Optimize Next.js applications for performance and SEO with image/font optimization, bundle optimization, caching, and Core Web Vitals improvements. Use when optimizing performance, improving SEO, or enhancing user experience.
---

# Next.js Optimization Specialist

Specialized in optimizing Next.js applications for performance, SEO, and Core Web Vitals.

## When to Use This Skill

- Optimizing images with next/image
- Optimizing fonts with next/font
- Reducing bundle size and code splitting
- Implementing lazy loading strategies
- Configuring caching strategies
- Improving SEO with metadata and sitemaps
- Optimizing Core Web Vitals (LCP, FID, CLS)

## Core Principles

- **Performance Budget**: Set and maintain performance targets
- **Measure First**: Use analytics to identify bottlenecks
- **Progressive Enhancement**: Build for slow connections first
- **Lazy Load**: Load resources only when needed
- **Cache Strategically**: Balance freshness and performance
- **SEO-Friendly**: Ensure search engines can index content

## Image Optimization

### next/image Component

```typescript
import Image from 'next/image'

// Responsive image
export const Hero = () => {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero image"
      width={1200}
      height={600}
      priority // WHY: Load above-the-fold images immediately
    />
  )
}

// Fill container
export const Avatar = () => {
  return (
    <div className="relative w-12 h-12">
      <Image
        src="/avatar.jpg"
        alt="User avatar"
        fill
        className="rounded-full object-cover"
      />
    </div>
  )
}

// Sizes for responsive images
export const ProductImage = () => {
  return (
    <Image
      src="/product.jpg"
      alt="Product"
      width={800}
      height={600}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    />
  )
}

// External images (requires configuration)
// next.config.js: images: { domains: ['example.com'] }
export const ExternalImage = () => {
  return (
    <Image
      src="https://example.com/image.jpg"
      alt="External image"
      width={400}
      height={300}
    />
  )
}
```

### Image Loader for CDN

```typescript
// next.config.js
module.exports = {
  images: {
    loader: 'custom',
    loaderFile: './lib/image-loader.ts',
  },
}

// lib/image-loader.ts
export default function imageLoader({
  src,
  width,
  quality,
}: {
  src: string
  width: number
  quality?: number
}) {
  return `https://cdn.example.com/${src}?w=${width}&q=${quality || 75}`
}
```

## Font Optimization

### next/font

```typescript
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
})

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  )
}

// tailwind.config.ts
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)'],
        mono: ['var(--font-roboto-mono)'],
      },
    },
  },
}

// Local fonts
import localFont from 'next/font/local'

const customFont = localFont({
  src: './fonts/CustomFont.woff2',
  display: 'swap',
  variable: '--font-custom',
})
```

## Bundle Optimization

### Code Splitting

```typescript
// Dynamic import for client components
import dynamic from 'next/dynamic'

// WHY: Load heavy component only when needed
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false, // Disable SSR for this component
})

// Named export
const DynamicComponent = dynamic(
  () => import('./components').then(mod => mod.SpecificComponent)
)

// With options
const DynamicModal = dynamic(() => import('./Modal'), {
  loading: () => <div>Loading...</div>,
  ssr: false,
})
```

### Tree Shaking

```typescript
// Bad: Imports entire library
import _ from 'lodash'

// Good: Import only what you need
import debounce from 'lodash/debounce'

// Better: Use ES modules
import { debounce } from 'lodash-es'
```

### Bundle Analysis

```bash
# Install bundle analyzer
npm install @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // Next.js config
})

# Analyze bundle
ANALYZE=true npm run build
```

## Caching Strategies

### Fetch Caching (App Router)

```typescript
// Static Generation (cached indefinitely)
const data = await fetch('https://api.example.com/data')

// Revalidate every 60 seconds (ISR)
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 },
})

// No caching (SSR)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',
})

// Tag-based revalidation
const data = await fetch('https://api.example.com/data', {
  next: { tags: ['users'] },
})

// Revalidate by tag
import { revalidateTag } from 'next/cache'
revalidateTag('users')
```

### Route Segment Config

```typescript
// app/dashboard/page.tsx
// Force dynamic rendering
export const dynamic = 'force-dynamic'
export const revalidate = 0

// Force static rendering
export const dynamic = 'force-static'

// Revalidate every hour
export const revalidate = 3600
```

## SEO Optimization

### Metadata API

```typescript
// app/layout.tsx - Static metadata
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: {
    default: 'My App',
    template: '%s | My App',
  },
  description: 'My awesome application',
  keywords: ['nextjs', 'react', 'typescript'],
  authors: [{ name: 'Your Name' }],
  openGraph: {
    title: 'My App',
    description: 'My awesome application',
    url: 'https://myapp.com',
    siteName: 'My App',
    images: [
      {
        url: 'https://myapp.com/og-image.jpg',
        width: 1200,
        height: 630,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'My App',
    description: 'My awesome application',
    images: ['https://myapp.com/twitter-image.jpg'],
  },
}

// app/blog/[slug]/page.tsx - Dynamic metadata
export async function generateMetadata({
  params,
}: {
  params: { slug: string }
}): Promise<Metadata> {
  const post = await fetchPost(params.slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
    },
  }
}
```

### Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await fetchAllPosts()

  const postEntries: MetadataRoute.Sitemap = posts.map(post => ({
    url: `https://myapp.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly',
    priority: 0.8,
  }))

  return [
    {
      url: 'https://myapp.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://myapp.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    ...postEntries,
  ]
}
```

### Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/admin/', '/api/'],
    },
    sitemap: 'https://myapp.com/sitemap.xml',
  }
}
```

## Core Web Vitals

### Largest Contentful Paint (LCP)

```typescript
// Optimize images
<Image
  src="/hero.jpg"
  alt="Hero"
  priority // Load immediately
  width={1200}
  height={600}
/>

// Preload critical resources
// app/layout.tsx
export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html>
      <head>
        <link rel="preload" href="/hero.jpg" as="image" />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### First Input Delay (FID)

```typescript
// Code splitting to reduce JavaScript
const HeavyComponent = dynamic(() => import('./HeavyComponent'))

// Use Server Components to reduce client JavaScript
// Server Component (no JS sent to client)
export default async function Page() {
  const data = await fetchData()
  return <DataDisplay data={data} />
}
```

### Cumulative Layout Shift (CLS)

```typescript
// Always specify image dimensions
<Image
  src="/image.jpg"
  alt="Image"
  width={400}  // WHY: Prevent layout shift
  height={300}
/>

// Reserve space for dynamic content
<div className="min-h-[200px]">
  {loading ? <Skeleton /> : <Content />}
</div>

// Use font-display: swap
const inter = Inter({
  subsets: ['latin'],
  display: 'swap', // Prevent invisible text during font load
})
```

## Performance Monitoring

```typescript
// app/layout.tsx - Web Vitals reporting
'use client'

import { useReportWebVitals } from 'next/web-vitals'

export function WebVitals() {
  useReportWebVitals((metric) => {
    console.log(metric)
    // Send to analytics
    analytics.track(metric.name, {
      value: metric.value,
      id: metric.id,
    })
  })

  return null
}
```

## Tools to Use

- `Read`: Read Next.js configuration and components
- `Edit`: Update configuration and components
- `Bash`: Run build and analyze bundle

### Bash Commands

```bash
# Build for production
npm run build

# Analyze bundle
ANALYZE=true npm run build

# Lighthouse audit
npx lighthouse https://yoursite.com --view

# Check build output
npm run build && ls -lh .next/static/chunks
```

## Workflow

1. **Measure Baseline**: Run Lighthouse audit
2. **Identify Issues**: Analyze Core Web Vitals
3. **Optimize Images**: Use next/image with proper sizing
4. **Optimize Fonts**: Use next/font with display: swap
5. **Reduce Bundle**: Code split and tree shake
6. **Configure Caching**: Set appropriate revalidation
7. **Add Metadata**: Implement SEO metadata
8. **Measure Again**: Verify improvements
9. **Monitor**: Set up ongoing monitoring

## Related Skills

- `nextjs-app-development`: For Next.js fundamentals
- `react-component-development`: For component optimization
- `playwright-testing`: For performance testing

## Key Reminders

- Use next/image for all images (automatic optimization)
- Use next/font for web fonts (automatic optimization)
- Implement code splitting with dynamic imports
- Set appropriate caching strategies (revalidate, tags)
- Generate metadata for all pages (SEO)
- Create sitemap.xml and robots.txt
- Monitor Core Web Vitals (LCP, FID, CLS)
- Analyze bundle size regularly
- Preload critical resources
- Use Server Components to reduce client JavaScript
- Implement proper loading states to prevent CLS
- Test on slow connections and low-end devices
- Write comments explaining WHY for optimization decisions
