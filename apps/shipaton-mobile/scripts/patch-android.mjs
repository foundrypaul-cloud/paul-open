import { readFile, writeFile } from 'node:fs/promises';

const path = new URL('../android/app/src/main/AndroidManifest.xml', import.meta.url);
let manifest = await readFile(path, 'utf8');

if (!manifest.includes('android:name=".MainActivity"')) {
  throw new Error('MainActivity was not found in AndroidManifest.xml');
}

manifest = manifest.replace(
  /(android:name="\.MainActivity"[\s\S]*?android:launchMode=")[^"]+(")/,
  '$1singleTop$2',
);

if (!manifest.includes('android:launchMode="singleTop"')) {
  throw new Error('RevenueCat launchMode patch did not apply');
}

await writeFile(path, manifest);
console.log('Android MainActivity launchMode is singleTop.');
