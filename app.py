import gradio as gr



from utils import seg_everything

def test(input_image):
    return input_image

# gr.Row() gr.Column()
with gr.Blocks(theme = gr.themes.Soft()) as demo:      
    with gr.Row(): 
        with gr.Column(): # input         
            input_image = gr.Image(type="numpy")
            with gr.Tab(label="Everything") as seg_everything_tab:  
                seg_everything_btn = gr.Button()                                             
            with gr.Tab(label="Box") as box_tab:  
                pass            
            
        with gr.Column():         
            output_image = gr.Image()                               
    seg_everything_btn.click(
        fn=seg_everything,
        inputs=[input_image],
        outputs=[input_image],
    )                                                                        
    # seg_everything_tab.select(
    #     fn = seg_everything,
    #     inputs=[input_image_component,],
    #     outputs = output_image_component,        
    # )   

        
                
demo.queue(max_size=5)  

if __name__ == "__main__":     
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7890,
        # share = True,
    )               
       
