# Finetuning Open Genmoji

Here's how you can finetune Open Genmoji yourself, either with a different set of emojis, finetune Open Genmoji with more steps, use a different model, or just for fun!

See the README in the `lora` folder for more information about what models have already been finetuned.

**This guide offers a way to finetune with SimpleTuner. Feel free to finetune with other methods and contribute to this repo!**

## Setting Up an Environment

In order to download emojis, you'll need to install a few packages. Feel free to use the `venv` you are using for running Open Genmoji in the root directory, or create a new one. Note that training with SimpleTuner will requiring cloning another repository into here, and thus require another `venv`.

Either way, ensure you have the following packages installed:

```
pip3 install requests pillow beautifulsoup4
```

## Gathering Data

First, you'll need to get the Emojis that you want to finetune on. In the end, you want a single directory with pairs of images and text descriptions of the image, like this:

```
trainingData/
├─ img1.txt
├─ img1.png
├─ img2.txt
├─ img2.png
├─ img3.txt
├─ img3.png

... and so on
```

This folder contains the files necessary to obtain this data, from [Emojigraph's Apple Emoji List](https://emojigraph.org/apple/). Here's what you'll need to do:

1. Run `getEmojiList.py`: This will download Emojigraph's list of all Apple Emojis, saving each emoji's PNG image link, its Emojigraph name, as well as its processed name into a `emojis.json`. Here's what that looks like:

   ```json
   [
   	{
   		"link": "https://emojigraph.org/media/apple/grinning-face_1f600.png",
   		"name": "grinning-face",
   		"processed": "grinning face emoji"
   	},
   	{
   		"link": "https://emojigraph.org/media/apple/grinning-face-with-big-eyes_1f603.png",
   		"name": "grinning-face-with-big-eyes",
   		"processed": "grinning face with big eyes emoji"
   	}
   	// and so on...
   ]
   ```

2. (Optional) Run `pruneEmojiList.py`: This will remove the skin color variants from the `emojis.json` list. This is intended to make the model run faster, although it also causes it to generate all emojis with the default Emoji bright yellow skin tone. It will make a new `emojisPruned.json` file.
3. Run `downloadEmojiList.py`: This will download all Emojis from a given list. By default it downloads from `emojiPruned.json`. You must change it to `emojis.json` if you wish to download the entire list. Note that this will take some time. It will result in a `emojis` folder (containing the training data pairs, with each emoji given a white background) and a `raw` folder (containing simply png versions of every emoji)

Now, all you need is the `emojis` folder.

## Setting Up SimpleTuner

Now, let's set up SimpleTuner in our repository to begin training.

```bash
git clone --branch=release https://github.com/bghira/SimpleTuner.git
cd SimpleTuner
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U poetry pip
poetry config virtualenvs.create false
```

Then, download the dependencies:

```bash
# MacOS
poetry install -C install/apple

# Linux
poetry install

# Linux with ROCM
poetry install -C install/rocm
```

The last thing we need to do is configure SimpleTuner for what we're doing. Go to the folder labelled `config`, in the directory this README is in. Replace the files in SimpleTuner's `config` folder with those in Open Genmoji's.

Now, you'll have to change some of the fields in the config. Feel free to change what you want, but here's what I recommend. Let's start with `config.json`:

What you'll need to change are the following lines:

- `--max_train_steps`: Set this to how many steps you want the AI to finetune for
- `--checkpointing_steps`: Set this to how many steps before it saves the current weights. It will also be able to leave off from the last checkpoint should it be prematurely terminated.
- `--checkpoints_total_limit`: How many checkpoints in total to save. It'll delete the oldest one if it passes it. Each checkpoint is big, but I recommend keeping quite a few in case you want to go back and avoid overfit
- `--pretrained_model_name_or_path`: What model to train. If you're not using Flux, you'll also have to change `--model_family`
- `--resolution` and `--validation_resolution`: Whatever your training data is. Emojigraph uses 160x160.

Then, in `multidatabackend.json`, change the following in the first element of the array (id `emojis`):

- `instance_data_dir`: An **absolute** path to whever your data is stored. (It should start with "/" on Mac)
- `minimum_image_size` and `resolution`: Given that each emoji is the same, these should be the same. Again, default Emojigraph is 160

## Running the Training

Now, you're ready to train! Simply run:

```bash
./train.sh
```

And it should start training. Note that you can quit and resume the training **from the last checkpoint** so be sure you have checkpoints in the config.

It will take quite a while (hours, up to days), but the result should be worth it!

You can monitor the validation image (a smiley face) and the checkpoints in `output/models`.

## Uploading Your Model to Open Genmoji

Optionally, help Open Genmoji expand!

When your training is done, go ahead and take your `pytorch_lora_weights.safetensors` **directly under output/models** (not in a checkpoint), give it a nice name, and upload it into the `lora` folder in the Open Genmoji repo with Git LFS. Then, add some metadata in the README. More instructions are there. With all that done, send in a PR! (I will sync it to HuggingFace)

Thank you for your contribution!
