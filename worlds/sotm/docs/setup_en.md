# Sentinels of the Multiverse Setup Guide

## Requirements Software

- Access to a way to play Sentinels of the Multiverse, such as physical cardboard and ink, the digital edition on Steam, or through Tabletop Simulator
- [Sentinels of the Multiverse CLI Client](https://github.com/Totox00/ap-sotm-client)

## General Concept

Since Sentinels of the Multiverse can be played as a board game, with the dedicated digital edition on Steam,
or on Tabletop Simulator, the client does not connect with the game itself. Instead, it will indicate what items you have received
and what locations are possible, and allow you to send those locations when you have accomplished them.

## Installing the Archipelago mod

Clone the repository linked above and follow the installation instructions.
Precompiled binaries are not currently available.

## Joining a MultiWorld Game

Once you have a compiled version of the client, simply launch it in a terminal and input the server address, server port, slot name, and password if applicable.
These values can also be provided using the -s, -p, -S, and -P flags respectively like `-p {port}`,
or set to the defaults by using those flags by not providing a value like `-P`
The defaults are:

| value          | flag | default        |
|----------------|------|----------------|
| server address | -s   | archipelago.gg |
| server port    | -p   | 38281          |
| slot name      | -S   | Player         | 
| password       | P    | (No password)  |

Once connected, you can move the cursor using arrow keys, send a location using Enter,
filter items and locations by typing, clear the filter using Ctrl+C, and disconnect using Ctrl+D.

Select can also be used to toggle multi-sending, which makes it so sending an Ultimate location for
a villain also sends the easier difficulties, and Advanced and Challenge also send the Normal location.

Home can be used to return to the top left if you get lost.

## Where do I get a config file?

The [Player Options](/games/Sentinels%20of%20the%20Multiverse/player-options) page on the website allows you to
configure your personal options and export them into a config file.
