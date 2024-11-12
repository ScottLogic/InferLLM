import React, {
  ChangeEvent,
  FormEvent,
  useCallback,
  useMemo,
  useState,
  useEffect,
  useRef,
} from 'react';
import styles from './input.module.css';
import RightArrowIcon from '../icons/send.svg';
import UploadIcon from '../icons/upload.svg';
import classNames from 'classnames';
import { Suggestions } from './suggestions';
 
export interface InputProps {
  sendMessage: (message: string) => void;
  waiting: boolean;
}
 
export const Input = ({ sendMessage, waiting }: InputProps) => {
  const [userInput, setUserInput] = useState<string>('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
 
  const onChange = useCallback((event: ChangeEvent<HTMLTextAreaElement>) => {
    setUserInput(event.target.value);
  }, []);
 
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const textareaHeight = textareaRef.current.scrollHeight;
     
      if (textareaHeight > 110) {
        textareaRef.current.style.height = '110px';
        textareaRef.current.style.overflowY = 'auto';
      } else {
        textareaRef.current.style.height = `${textareaHeight}px`;
        textareaRef.current.style.overflowY = 'hidden';
      }
    }
  }, [userInput]);
 
 
  const onSend = useCallback(
    (event: FormEvent<HTMLElement>) => {
      event.preventDefault();
      sendMessage(userInput);
      setUserInput('');
    },
    [sendMessage, userInput],
  );
 
  const sendDisabled = useMemo(() => userInput.length === 0, [userInput]);
 
  return (
    <>
      <form onSubmit={onSend} className={styles.inputContainer}>
      <textarea
          className={styles.textarea}
          ref={textareaRef}
          placeholder="Send a Message..."
          value={userInput}
          onChange={onChange}
          rows={1}
        />
        <div className={classNames(styles.uploadButton_container, { [styles.disabled]: sendDisabled })}>
        <button
        className={classNames(styles.uploadButton, { [styles.disabled]: sendDisabled })}
        disabled={sendDisabled}
      >
        <img src={UploadIcon} />
      </button>
      </div>
      <div className={classNames(styles.sendButton_container, { [styles.disabled]: sendDisabled })}>
        <button
        className={classNames(styles.sendButton, { [styles.disabled]: sendDisabled })}
        onClick={onSend}
        disabled={sendDisabled}>
        <img src={RightArrowIcon}/>
        </button>
        </div>
      </form>
      <Suggestions loadPrompt={setUserInput} waiting={waiting} />
    </>
  );
};
 