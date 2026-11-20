import { access, copyFile, cp, mkdir } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const appDir = fileURLToPath(new URL(".", import.meta.url));
const brandingDir = resolve(appDir, "../src/sen4cap_client/app/branding");
const [buildPath, outputPath, licensePath] = process.argv.slice(2);
const buildDir = buildPath
  ? resolve(buildPath)
  : join(appDir, "build/eozilla");
const outputDir = outputPath ? resolve(outputPath) : join(appDir, "dist");

// Copy the production UI files. Supply our own config and branding.
const uiFiles = [
  "index.html",
  "assets",
  "eozilla-small.svg",
  "eozilla.svg",
  "privacy.md",
];
const eozillaLicense = licensePath
  ? resolve(licensePath)
  : resolve(appDir, "../../eozilla/eozilla-app/LICENSE");
const sources = [
  ...uiFiles.map((name) => [join(buildDir, name), name]),
  [join(appDir, "config.json"), "config.json"],
  [join(brandingDir, "favicon.ico"), "branding/favicon.ico"],
  [join(brandingDir, "icon.png"), "branding/icon.png"],
  [resolve(appDir, "../LICENSE"), "sen4cap-license.txt"],
  [eozillaLicense, "eozilla-license.txt"],
];

try {
  await Promise.all(sources.map(([source]) => access(source)));
  await mkdir(outputDir);
  await mkdir(join(outputDir, "branding"));
  await Promise.all(
    sources.map(([source, name]) =>
      name === "assets"
        ? cp(source, join(outputDir, name), { recursive: true })
        : copyFile(source, join(outputDir, name)),
    ),
  );
  console.log(`Static app assembled at ${outputDir}`);
} catch (error) {
  console.error(`Unable to assemble the static app. ${error.message}`);
  process.exitCode = 1;
}
