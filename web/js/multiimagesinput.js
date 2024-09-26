import { app } from "/scripts/app.js";

app.registerExtension({
    name: "ComfyUI/Pixtral Vision.MultiImagesInput",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "MultiImagesInput") {
            nodeType.prototype.onNodeCreated = function () {
                this.addWidget("button", "Update inputs", null, () => {
                    this.updateInputs();
                });
            };

            nodeType.prototype.updateInputs = function () {
                const targetNumberOfInputs = this.widgets.find(
                    (w) => w.name === "inputcount"
                ).value;

                // Remove extra inputs
                while (this.inputs.length > targetNumberOfInputs) {
                    this.removeInput(this.inputs.length - 1);
                }

                // Add new inputs
                while (this.inputs.length < targetNumberOfInputs) {
                    this.addInput(`image_${this.inputs.length + 1}`, "IMAGE");
                }

                // Trigger a node size recalculation
                this.size = this.computeSize();
                this.setDirtyCanvas(true, true);
            };

            // Override the onConnectionsChange method
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
                if (onConnectionsChange) {
                    onConnectionsChange.apply(this, arguments);
                }
                this.updateInputs();
            };
        }
    }
});