import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
  name: "Comfy.PixtralVision.PreviewText",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "preview_text") {
      // Add custom widget
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

        // Add a text widget for preview
        const widget = ComfyWidgets.STRING(this, "display_text", ["STRING", { multiline: true }], app);
        widget.widget.inputEl.readOnly = true;
        widget.widget.inputEl.style.color = "rgba(255, 255, 255, 0.9)";  // 90% white
        widget.widget.inputEl.style.fontSize = "16px";
        widget.widget.inputEl.style.padding = "8px";
        widget.widget.inputEl.style.lineHeight = "1.4";
        widget.widget.inputEl.style.fontFamily = "monospace";

        return r;
      };

      // Handle node execution
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, arguments);
        const text = message.text;
        
        if (Array.isArray(text)) {
          // Find the display widget
          const widget = this.widgets.find((w) => w.name === "display_text");
          if (widget) {
            widget.value = text.join("\n");
          }
        }

        // Resize node
        requestAnimationFrame(() => {
          const sz = this.computeSize();
          if (sz[0] < this.size[0]) sz[0] = this.size[0];
          if (sz[1] < this.size[1]) sz[1] = this.size[1];
          this.onResize?.(sz);
          app.graph.setDirtyCanvas(true, false);
        });
      };
    }
  },
});
