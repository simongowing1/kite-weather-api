import { Suspense } from 'react';
import KiteViewer from '@/components/KiteViewer';

export default function Home() {
  return (
    <Suspense>
      <KiteViewer />
    </Suspense>
  );
}
