import { visit } from 'unist-util-visit';
import { h } from 'hastscript';

// This plugin transforms :::en and :::zh container directives into div elements
export function remarkBilingualDirective() {
  return (tree) => {
    visit(tree, (node) => {
      if (node.type === 'containerDirective') {
        if (node.name === 'en' || node.name === 'zh') {
          const data = node.data || (node.data = {});
          const tagName = 'div';

          data.hName = tagName;
          data.hProperties = h(tagName, { class: `lang-${node.name}` }).properties;
        }
      }
    });
  };
}
