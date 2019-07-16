#!/usr/bin/env bash

# Check if ~/.nano directory exists
if [ ! -d "$HOME/.nano" ]; then
    echo "Creating ~/.nano directory..."
    mkdir ~/.nano
fi

# Copy nari.nanorc to ~/.nano
echo "Copying nari.nanorc to ~/.nano"
cp nari.nanorc ~/.nano/nari.nanorc

# Add nari.nanorc to .nanorc
echo "include $HOME/.nano/nari.nanorc" >> ~/.nanorc
