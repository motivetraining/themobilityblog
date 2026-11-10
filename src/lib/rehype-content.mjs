// Rehype plugin for images and tables written in post and page Markdown.
//
// Images: Markdown has no way to say how big an image is, so the browser can't
// reserve space for it and the text jumps when it loads. This reads the real
// dimensions from the file in public/ and adds width/height, plus lazy loading
// so images further down a post don't compete with the featured image.
//
// Tables: wrapped in a scrolling container, so a wide table scrolls sideways
// on a phone instead of pushing the whole page wider than the screen.
import { existsSync } from "node:fs";
import { join } from "node:path";

export function rehypeContent() {
  return async (tree) => {
    const images = [];
    const walk = (node) => {
      if (!node.children) return;
      node.children = node.children.map((child) => {
        if (child.type !== "element") return child;
        if (child.tagName === "img") images.push(child);
        if (child.tagName === "table") {
          return { type: "element", tagName: "div", properties: { className: ["table-scroll"] }, children: [child] };
        }
        walk(child);
        return child;
      });
    };
    walk(tree);

    for (const img of images) {
      const p = img.properties ?? (img.properties = {});
      p.loading ??= "lazy";
      p.decoding ??= "async";
      const src = typeof p.src === "string" ? p.src : "";
      if (!src.startsWith("/") || p.width || p.height) continue;
      const file = join(process.cwd(), "public", decodeURIComponent(src));
      if (!existsSync(file)) continue;
      try {
        const { default: sharp } = await import("sharp");
        const { width, height } = await sharp(file).metadata();
        p.width = width;
        p.height = height;
      } catch {
        // Unreadable image (or sharp unavailable): leave it without dimensions
        // rather than fail the build.
      }
    }
  };
}
