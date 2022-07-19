from io import BytesIO
buffer = BytesIO()
import numpy as np
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

def process_wordcloud(text, **kwargs):
    """
    Function for generating wordcloud object
    Parameters
    ----------
    text: string
        Text to be converted to a wordcloud
    font_path : string
        Font path to the font that will be used (OTF or TTF).
        Defaults to DroidSansMono path on a Linux machine. If you are on
        another OS or don't have this font, you need to adjust this path.
    width : int (default=400)
        Width of the canvas.
    height : int (default=200)
        Height of the canvas.
    prefer_horizontal : float (default=0.90)
        The ratio of times to try horizontal fitting as opposed to vertical.
        If prefer_horizontal < 1, the algorithm will try rotating the word
        if it doesn't fit. (There is currently no built-in way to get only
        vertical words.)
    mask : nd-array or None (default=None)
        If not None, gives a binary mask on where to draw words. If mask is not
        None, width and height will be ignored and the shape of mask will be
        used instead. All white (#FF or #FFFFFF) entries will be considerd
        "masked out" while other entries will be free to draw on. [This
        changed in the most recent version!]
    contour_width: float (default=0)
        If mask is not None and contour_width > 0, draw the mask contour.
    contour_color: color value (default="black")
        Mask contour color.
    scale : float (default=1)
        Scaling between computation and drawing. For large word-cloud images,
        using scale instead of larger canvas size is significantly faster, but
        might lead to a coarser fit for the words.
    min_font_size : int (default=4)
        Smallest font size to use. Will stop when there is no more room in this
        size.
    font_step : int (default=1)
        Step size for the font. font_step > 1 might speed up computation but
        give a worse fit.
    max_words : number (default=200)
        The maximum number of words.
    stopwords : set of strings or None
        The words that will be eliminated. If None, the build-in STOPWORDS
        list will be used. Ignored if using generate_from_frequencies.
    background_color : color value (default="black")
        Background color for the word cloud image.
    max_font_size : int or None (default=None)
        Maximum font size for the largest word. If None, height of the image is
        used.
    mode : string (default="RGB")
        Transparent background will be generated when mode is "RGBA" and
        background_color is None.
    relative_scaling : float (default='auto')
        Importance of relative word frequencies for font-size.  With
        relative_scaling=0, only word-ranks are considered.  With
        relative_scaling=1, a word that is twice as frequent will have twice
        the size.  If you want to consider the word frequencies and not only
        their rank, relative_scaling around .5 often looks good.
        If 'auto' it will be set to 0.5 unless repeat is true, in which
        case it will be set to 0.
        .. versionchanged: 2.0
            Default is now 'auto'.
    color_func : callable, default=None
        Callable with parameters word, font_size, position, orientation,
        font_path, random_state that returns a PIL color for each word.
        Overwrites "colormap".
        See colormap for specifying a matplotlib colormap instead.
        To create a word cloud with a single color, use
        ``color_func=lambda *args, **kwargs: "white"``.
        The single color can also be specified using RGB code. For example
        ``color_func=lambda *args, **kwargs: (255,0,0)`` sets color to red.
    regexp : string or None (optional)
        Regular expression to split the input text into tokens in process_text.
        If None is specified, ``r"\w[\w']+"`` is used. Ignored if using
        generate_from_frequencies.
    collocations : bool, default=True
        Whether to include collocations (bigrams) of two words. Ignored if using
        generate_from_frequencies.
        .. versionadded: 2.0
    colormap : string or matplotlib colormap, default="viridis"
        Matplotlib colormap to randomly draw colors from for each word.
        Ignored if "color_func" is specified.
        .. versionadded: 2.0
    normalize_plurals : bool, default=True
        Whether to remove trailing 's' from words. If True and a word
        appears with and without a trailing 's', the one with trailing 's'
        is removed and its counts are added to the version without
        trailing 's' -- unless the word ends with 'ss'. Ignored if using
        generate_from_frequencies.
    repeat : bool, default=False
        Whether to repeat words and phrases until max_words or min_font_size
        is reached.
    include_numbers : bool, default=False
        Whether to include numbers as phrases or not.
    min_word_length : int, default=0
        Minimum number of letters a word must have to be included.
    collocation_threshold: int, default=30
        Bigrams must have a Dunning likelihood collocation score greater than this
        parameter to be counted as bigrams. Default of 30 is arbitrary.
        See Manning, C.D., Manning, C.D. and Schütze, H., 1999. Foundations of
        Statistical Natural Language Processing. MIT press, p. 162
        https://nlp.stanford.edu/fsnlp/promo/colloc.pdf#page=22

    Notes
    -----
    Larger canvases make the code significantly slower. If you need a
    large word cloud, try a lower canvas size, and set the scale parameter.
    The algorithm might give more weight to the ranking of the words
    than their actual frequencies, depending on the ``max_font_size`` and the
    scaling heuristic.

    Returns
    -------
    buffer: io.BytesIO
        buffer containing the generated wordcloud image in bytes
    """

    if text is None:
        text = "Sample Text"

    wordcloud_obj = WordCloud(**kwargs).generate(text)
    wordcloud_buff = plot_cloud_buff(wordcloud_obj)
    return wordcloud_buff

def plot_cloud_buff(wordcloud_obj):
    """
    Function to get generated wordcloud in bytes

    Parameters
    ----------
    wordcloud_obj: wordcloud.WordCloud
        The generated wordcloud object

    Returns
    -------
    buffer: io.BytesIO
        buffer containing the generated wordcloud image in bytes
    """

    plt.figure(figsize=(wordcloud_obj.width/100,wordcloud_obj.height/100))
    plt.imshow(wordcloud_obj) 
    plt.axis("off")
    plt.savefig(buffer,format='png', bbox_inches='tight', pad_inches=0)
    return buffer

def get_image_from_buffer(buffer):
    """
    Function to convert wordcloud buffer to PIL.Image

    Parameters
    ----------
    buffer: io.BytesIO
        buffer containing the generated wordcloud image in bytes

    Returns
    -------
    PIL.Image
    """

    buffer.seek(0)
    return Image.open(buffer)

def fit_to_canvas(image, canvas_size):
    """
    Helper function to resize wordcloud mask to canvas
    
    Parameters
    ----------
    image: PIL.Image
        Wordcloud mask
    canvas_size: (int, int)
        Size of the canvas to which the image is fit

    Returns
    -------
    PIL.Image
    """

    width = image.size[0]
    height = image.size[1]
    maxwidth = canvas_size[0]
    maxheight = canvas_size[1]
    resize_ratio = min(maxwidth/width, maxheight/height)
    return image.resize((int(width*resize_ratio), int(height*resize_ratio)), Image.ANTIALIAS)

def prep_mask(image, canvas_size=None):
    """
    Helper function to prepare wordcloud mask
    
    Parameters
    ----------
    image: PIL.Image
        Wordcloud mask
    canvas_size: (int, int)
        Size of the canvas to which the image is fit   

    Returns
    -------
    numpy.ndarray
    """
    if canvas_size is None:
        canvas_size = image.size

    new_image = Image.new("RGBA", canvas_size, "WHITE") # Create a white rgba background
    image = image.convert("RGBA")
    image = fit_to_canvas(image, canvas_size) # Resize mask to fit canvas
    offset = ((new_image.size[0] - image.size[0]) // 2, (new_image.size[1] - image.size[1]) // 2) # Center mask onto canvas
    new_image.paste(image, offset, image)
    return np.asarray(new_image)

################################## UI ##############################################

def st_ui():
    wc_bg_color = st.sidebar.color_picker('Background Color', value='#FFF')
    wc_contour_color = "#%06X" % (0xFFFFFF ^ int(wc_bg_color[1:], 16))
    wc_quality = st.sidebar.selectbox("Quality", ["Low", "Medium", "High"], index=1)
    quality_to_dim = {
        "Low": {
            "width": 640,
            "height": 480
        },
        "Medium": {
            "width": 1280,
            "height": 720
        },
        "High": {
            "width": 1920,
            "height": 1080
        },
    }
    wc_try_mask = st.sidebar.checkbox('Try WordCloud Mask', help='Unselect if you want to upload custom Word Cloud mask')
    wc_mask = st.sidebar.file_uploader('Or upload Custom WordCloud Mask', type=["png","jpg","jpeg"], help="All white (#FF or #FFFFFF) entries will be considerd “masked out” while other entries will be free to draw on.")

    if wc_try_mask:
        wc_mask_img = Image.open("./resources/example_mask.png")
        wc_mask_array = prep_mask(wc_mask_img, canvas_size=(quality_to_dim[wc_quality]['width'], quality_to_dim[wc_quality]['height']))
    elif wc_mask is not None:
        wc_mask_img = Image.open(wc_mask)
        wc_mask_array = prep_mask(wc_mask_img, canvas_size=(quality_to_dim[wc_quality]['width'], quality_to_dim[wc_quality]['height']))
    else:
        wc_mask_array = None


    st.subheader("WordCloud Generator")
    my_text = st.text_area("Text to convert to WordCloud", open("./resources/example_text.txt", "r").read())
    if wc_mask_array is not None:
        st.sidebar.write("Selected WordCloud Mask")
        st.sidebar.image(wc_mask_array)

    if st.button("Generate"):
        wordcloud_img = process_wordcloud(my_text, mask=wc_mask_array, width=quality_to_dim[wc_quality]['width'], height=quality_to_dim[wc_quality]['height'], background_color=wc_bg_color, stopwords = STOPWORDS, contour_width=0.5, contour_color=wc_contour_color)
        st.image(wordcloud_img)
        st.download_button(
            label="Download Image",
            data=wordcloud_img,
            file_name="wordcloud.png",
            mime="image/jpeg")

if __name__ == "__main__":
    st_ui()