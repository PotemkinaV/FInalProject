import torch
from transformers import BertForSequenceClassification, BertTokenizer

from src.config import CLASSES, MODEL_PATH

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def init_model():
    # load model
    model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
    model.to(device)
    model.eval()
    model.zero_grad()
    return model


def init_tokenizer():
    # load tokenizer
    tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
    return tokenizer


def predict(model, tokenizer, text):
    # get special tokens
    ref_token_id = tokenizer.pad_token_id  # A token used for generating token reference
    sep_token_id = tokenizer.sep_token_id  # A token used as a separator between question and text and it is also added to the end of the text.
    cls_token_id = tokenizer.cls_token_id  # A token used for prepending to the concatenated question-text word sequence

    # construct input and reference pair
    input_ids, ref_input_ids, sep_id = construct_input_ref_pair(tokenizer, text,
                                                                [ref_token_id,
                                                                 sep_token_id,
                                                                 cls_token_id])

    score = model(input_ids)[0]
    label = torch.argmax(score[0]).cpu().detach().numpy()
    label = CLASSES[int(label)]
    return label


def construct_input_ref_pair(tokenizer, text, special_tokens):
    ref_token_id, sep_token_id, cls_token_id = special_tokens
    text_ids = tokenizer.encode(
        text,
        add_special_tokens=True,
        max_length=512,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt',
        truncation=True
    ).squeeze(0).tolist()
    ref_input_ids = [cls_token_id] + [ref_token_id] * (len(text_ids) - 2) + [
        sep_token_id]
    return torch.tensor([text_ids], device=device), torch.tensor([ref_input_ids],
                                                                 device=device), len(
        text_ids)


def construct_input_ref_token_type_pair(input_ids, sep_ind=0):
    """
    Constructs token_type_ids and ref_token_type_ids based on input_ids and sep_ind.

    Args:
        input_ids (torch.Tensor): The input ids.
        sep_ind (int, optional): The index of the separator. Defaults to 0.

    Returns:
        tuple: A tuple containing token_type_ids and ref_token_type_ids.
    """
    seq_len = input_ids.size(1)

    # Construct token_type_ids
    token_type_ids = torch.tensor([[0 if i <= sep_ind else 1 for i in range(seq_len)]],
                                  device=device)

    # Construct ref_token_type_ids
    ref_token_type_ids = torch.zeros_like(token_type_ids, device=device)

    return token_type_ids, ref_token_type_ids


def construct_input_ref_pos_id_pair(input_ids):
    """
    Constructs position and reference position IDs for input IDs.

    Args:
        input_ids (torch.Tensor): Input IDs.

    Returns:
        tuple: Position IDs and reference position IDs.
    """
    # Get the sequence length
    seq_length = input_ids.size(1)

    # Generate position IDs
    position_ids = torch.arange(seq_length, dtype=torch.long, device=device)

    # Generate reference position IDs
    ref_position_ids = torch.zeros(seq_length, dtype=torch.long, device=device)

    # Expand position and reference position IDs to match input IDs shape
    position_ids = position_ids.unsqueeze(0).expand_as(input_ids)
    ref_position_ids = ref_position_ids.unsqueeze(0).expand_as(input_ids)

    return position_ids, ref_position_ids


def construct_attention_mask(input_ids):
    return torch.ones_like(input_ids)
