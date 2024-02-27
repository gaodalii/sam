import gradio as gr



from utils import seg_everything

def test(input_image):
    return input_image

# gr.Row() gr.Column()
with gr.Blocks(theme = gr.themes.Soft()) as demo:      
    with gr.Column():    
        image_component = gr.Image(type="numpy")      
        # with gr.Column(): # input         
        with gr.Tab(label="Everything") as seg_everything_tab:  
            seg_everything_btn = gr.Button()                                             
        with gr.Tab(label="Box") as box_tab:  
            pass            
                                             
    seg_everything_btn.click(
        fn=seg_everything,
        inputs=[image_component],
        outputs=[image_component],
    )                                                                        

                        
demo.queue(max_size=5)  

if __name__ == "__main__":     
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7890,
    )                      
