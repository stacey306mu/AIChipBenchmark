git push --set-upstream origin yb/add_transformer_block_testimport torch
import torch.nn as nn
import time
from blocks.encoder_layer import EncoderLayer
from blocks.decoder_layer import DecoderLayer
from layers.multi_head_attention import MultiHeadAttention
from layers.layer_norm import LayerNorm
from layers.position_wise_feed_forward import PositionwiseFeedForward


def test_transformer_encoder_block(d_model, n_head, ffn_hidden, batch_size, seq_len, num_iterations):

    transformer_encoder_block = EncoderLayer (d_model, ffn_hidden, n_head, drop_prob = 0.1).cuda()
    input_tensor = torch.rand(batch_size, seq_len, d_model).cuda()
    
    # warm up
    for i in range(20):
        output_tensor = transformer_encoder_block(input_tensor, None)

   # test 
    start_time = time.time()
    for i in range(num_iterations):
        output_tensor = transformer_encoder_block(input_tensor, None)
    end_time = time.time()
    print("Time per iteration: {:.6f} seconds".format((end_time - start_time) / num_iterations))


def test_transformer_decoder_block(d_model, n_head, ffn_hidden, batch_size, tgt_len, memory_len, num_iterations):
    transformer_decoder_block = DecoderLayer(d_model, ffn_hidden, n_head, drop_prob = 0.1).cuda()
    tgt_tensor = torch.rand(batch_size, tgt_len, d_model).cuda()
    memory_tensor = torch.rand(batch_size, memory_len, d_model).cuda()

    # warm up
    for i in range(20):
        output_tensor = transformer_decoder_block(tgt_tensor, memory_tensor, None, None)

   # test 
    start_time = time.time()
    for i in range(num_iterations):
        output_tensor = transformer_decoder_block(tgt_tensor, memory_tensor, None, None)
    end_time = time.time()

    print("Time per iteration: {:.6f} seconds".format((end_time - start_time) / num_iterations))

# test
test_transformer_encoder_block(d_model=512, n_head=8, ffn_hidden=2048, batch_size=32, seq_len=512, num_iterations=100)
test_transformer_decoder_block(d_model=512, n_head=8, ffn_hidden=2048, batch_size=32, tgt_len=512, memory_len=512, num_iterations=100)


